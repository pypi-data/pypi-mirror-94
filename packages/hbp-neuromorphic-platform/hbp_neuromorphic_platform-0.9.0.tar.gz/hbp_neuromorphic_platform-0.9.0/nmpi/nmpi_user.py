"""
Client for interacting with the Neuromorphic Computing Platform of the Human Brain Project.

Authors: Andrew P. Davison, Domenico Guarino, UNIC, CNRS


Copyright 2016-2020 Andrew P. Davison and Domenico Guarino, Centre National de la Recherche Scientifique

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

"""

import os.path
import json
import getpass
import logging
import uuid
import time
try:
    from urlparse import urlparse
    from urllib import urlretrieve, urlencode
except ImportError:  # Py3
    from urllib.parse import urlparse, urlencode
    from urllib.request import urlretrieve
import errno
import fnmatch
import mimetypes
import requests
from requests.auth import AuthBase
try:
    from jupyter_collab_storage import oauth_token_handler  # v1
    have_collab_token_handler = True
except ImportError:
    try:
        from clb_nb_utils import oauth as oauth_token_handler  # v2
        have_collab_token_handler = True
    except ImportError:
        have_collab_token_handler = False
try:
    from hbp_service_client.storage_service.client import Client as StorageClient
    from hbp_service_client.storage_service.exceptions import StorageException
    have_collab_client = True
except ImportError:
    have_collab_client = False

mimetypes.init()
logger = logging.getLogger("NMPI")

IDENTITY_SERVICE_V1 = "https://services.humanbrainproject.eu/idm/v1/api"
IDENTITY_SERVICE_V2 = "https://iam.ebrains.eu/auth/realms/hbp/protocol/openid-connect"
COLLAB_SERVICE_V1 = "https://services.humanbrainproject.eu/collab/v0"
COLLAB_SERVICE_V2 = "https://wiki.ebrains.eu/rest/v1/"

TOKENFILE = os.path.expanduser("~/.hbptoken")


class HBPAuth(AuthBase):
    """Attaches OIDC Bearer Authentication to the given Request object."""

    def __init__(self, token):
        # setup any auth-related data here
        self.token = token

    def __call__(self, r):
        # modify and return the request
        r.headers['Authorization'] = 'Bearer ' + self.token
        return r


def _mkdir_p(path):
    # not needed in Python >= 3.2, use os.makedirs(path, exist_ok=True)
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


class Client(object):
    """
    Client for interacting with the Neuromorphic Computing Platform of
    the Human Brain Project.

    This includes submitting jobs, tracking job status and retrieving the
    results of completed jobs.

    *Arguments*:
        :username, password: credentials for accessing the platform.
            Not needed in Jupyter notebooks within the HBP Collaboratory.
        :job_service: the base URL of the platform Job Service.
            Generally the default value should be used.
        :quotas_service: the base URL of the platform Quotas Service.
            Generally the default value should be used.
        :token: when you authenticate with username and password, you will receive
            a token which can be used in place of the password until it expires.
        :verify: in case of problems with SSL certificate verification, you can
            set this to False, but this is not recommended.
    """

    def __init__(self, username=None,
                 password=None,
                 job_service="https://nmpi.hbpneuromorphic.eu/api/v2/",
                 quotas_service="https://quotas.hbpneuromorphic.eu",
                 token=None,
                 verify=True):
        if password is None and token is None:
            if have_collab_token_handler:
                # if are we running in a Jupyter notebook within the Collaboratory
                # the token is already available
                token = oauth_token_handler.get_token()
            elif os.path.exists(TOKENFILE):  # check for a stored token
                with open(TOKENFILE) as fp:
                    token_config = json.load(fp).get(username, None)
                    if token_config:
                        token = token_config["access_token"]
                    else:
                        password = getpass.getpass()
            else:
                # prompt for password
                password = getpass.getpass()

        self.username = username
        self.cert = None
        self.verify = verify
        self.token = token
        self.sleep_interval = 2.0
        (scheme, netloc, path, params, query, fragment) = urlparse(job_service)
        self.job_server = "%s://%s" % (scheme, netloc)
        self.quotas_server = quotas_service
        self.storage_client = None
        self.collab_source_folder = "source_code"  # remote folder into which code may be uploaded

        # if a token has been given, no need to authenticate
        if not self.token:
            self._hbp_auth(username, password)
        self.auth = HBPAuth(self.token)
        try:
            self._get_user_info()
        except Exception as err:
            if "invalid_token" in str(err):
                password = getpass.getpass()
                self._hbp_auth(username, password)
                self.auth = HBPAuth(self.token)
                self._get_user_info()
            else:
                raise

        if not have_collab_token_handler:
            # no need to cache the token if running in the Collaboratory
            with open(TOKENFILE, "w") as fp:
                json.dump({username: {"access_token": self.token}}, fp)

        # get schema
        req = requests.get(job_service, cert=self.cert, verify=self.verify, auth=self.auth)
        if req.ok:
            self._schema = req.json()
            self.resource_map = {name: entry["list_endpoint"]
                                 for name, entry in req.json().items()}
        else:
            self._handle_error(req)

    def _hbp_auth(self, username, password):
        """
        """
        # todo: add support for v2
        redirect_uri = self.job_server + '/complete/hbp/'

        self.session = requests.Session()
        # 1. login button on NMPI
        rNMPI1 = self.session.get(self.job_server + "/login/hbp/?next=/config.json",
                                  allow_redirects=False, verify=self.verify)
        # 2. receives a redirect
        if rNMPI1.status_code == 302:
            # Get its new destination (location)
            url = rNMPI1.headers.get('location')
            # https://services.humanbrainproject.eu/oidc/authorize?
            #   scope=openid%20profile
            #   state=jQLERcgK1xTDHcxezNYnbmLlXhHgJmsg
            #   redirect_uri=https://neuromorphic.humanbrainproject.eu/complete/hbp-oauth2/
            #   response_type=code
            #   client_id=nmpi
            # get the exchange cookie
            cookie = rNMPI1.headers.get('set-cookie').split(";")[0]
            self.session.headers.update({'cookie': cookie})
            # 3. request to the provided url at HBP
            rHBP1 = self.session.get(url, allow_redirects=False, verify=self.verify)
            # 4. receives a redirect to HBP login page
            if rHBP1.status_code == 302:
                # Get its new destination (location)
                url = rHBP1.headers.get('location')
                cookie = rHBP1.headers.get('set-cookie').split(";")[0]
                self.session.headers.update({'cookie': cookie})
                # 5. request to the provided url at HBP
                rHBP2 = self.session.get(url, allow_redirects=False, verify=self.verify)
                # 6. HBP responds with the auth form
                if rHBP2.text:
                    # 7. Request to the auth service url
                    formdata = {
                        'j_username': username,
                        'j_password': password,
                        'submit': 'Login',
                        'redirect_uri': redirect_uri + '&response_type=code&client_id=nmpi'
                    }
                    headers = {'accept': 'application/json'}
                    rNMPI2 = self.session.post("https://services.humanbrainproject.eu/oidc/j_spring_security_check",
                                               data=formdata,
                                               allow_redirects=True,
                                               verify=self.verify,
                                               headers=headers)
                    # check good communication
                    if rNMPI2.status_code == requests.codes.ok:
                        # check success address
                        if rNMPI2.url == self.job_server + '/config.json':
                            # print rNMPI2.text
                            res = rNMPI2.json()
                            self.token = res['auth']['token']['access_token']
                            self.config = res
                        # unauthorized
                        else:
                            if 'error' in rNMPI2.url:
                                raise Exception("Authentication Failure: No token retrieved." + rNMPI2.url)
                            else:
                                raise Exception("Unhandled error in Authentication." + rNMPI2.url)
                    else:
                        raise Exception("Communication error. Status code {} from HBP, expected 200".format(rNMPI2.status_code))
                else:
                    raise Exception("Something went wrong. No text.")
            else:
                raise Exception("Something went wrong. Status code {} from HBP, expected 302".format(rHBP1.status_code))
        else:
            raise Exception("Something went wrong. Status code {} from NMPI, expected 302".format(rNMPI1.status_code))

    def _get_user_info(self):
        req = requests.get(IDENTITY_SERVICE_V1 + "/user/me",
                           auth=self.auth)
        if req.ok:
            self.user_info = req.json()
        else:
            req2 = requests.get(IDENTITY_SERVICE_V2 + "/userinfo",
                                auth=self.auth)
            if req2.ok:
                self.user_info = req2.json()
                self.user_info["id"] = self.user_info.get("preferred_username", self.user_info["sub"])
                self.user_info["username"] = self.user_info.get("preferred_username", "unknown")
            else:
                self._handle_error(req)  # todo: need to somehow combine req and req2 here
        if self.username:
            assert self.user_info['username'] == self.username
        else:
            self.username = self.user_info['username']

    def _handle_error(self, request):
        """
        Deal with requests that return an error code (404, 500, etc.)
        """
        try:
            errmsg = request.json()["error_message"]
        except KeyError:
            errmsg = request.json()["error"]
        except ValueError:
            errmsg = request.content
        if isinstance(errmsg, bytes):
            errmsg = errmsg.decode('utf-8')
        logger.error(errmsg)
        raise Exception("Error %s: %s" % (request.status_code, errmsg))

    def _query(self, resource_uri, verbose=False, ignore404=False):
        """
        Retrieve a resource or list of resources.
        """
        req = requests.get(resource_uri, auth=self.auth,
                           cert=self.cert, verify=self.verify)
        if req.ok:
            if "objects" in req.json():
                objects = req.json()["objects"]
                if verbose:
                    return objects
                else:
                    return [obj["resource_uri"] for obj in objects]
            else:
                return req.json()
        elif ignore404 and req.status_code == 404:
            return None
        else:
            self._handle_error(req)

    def _post(self, resource_uri, data):
        """
        Create a new resource.
        """
        req = requests.post(resource_uri,
                            data=json.dumps(data),
                            auth=self.auth,
                            cert=self.cert, verify=self.verify,
                            headers={"content-type": "application/json"})
        if not req.ok:
            self._handle_error(req)
        if 'Location' in req.headers:
            return req.headers['Location']
        else:
            return req.json()

    def _put(self, resource_uri, data):
        """
        Updates a resource.
        """
        req = requests.put(resource_uri,
                           data=json.dumps(data),
                           auth=self.auth,
                           cert=self.cert, verify=self.verify,
                           headers={"content-type": "application/json"})
        if not req.ok:
            self._handle_error(req)
        return data

    def _delete(self, resource_uri):
        """
        Deletes a resource
        """
        req = requests.delete(resource_uri,
                              auth=self.auth,
                              cert=self.cert, verify=self.verify)
        if not req.ok:
            self._handle_error(req)

    def submit_job(self, source, platform, collab_id, config=None, inputs=None,
                   command="run.py {system}", tags=None, wait=False):
        """
        Submit a job to the platform.

        *Arguments*:
            :source: the Python script to be run, the URL of a public version
                control repository containing Python code, a zip file
                containing Python code, or a local directory containing
                Python code.
            :platform: the neuromorphic hardware system to be used.
                Either "BrainScaleS" or "SpiNNaker".
            :collab_id: the ID of the collab to which the job belongs
            :config: (optional) a dictionary containing configuration information
                for the hardware platform. See the Platform Guidebook for
                more details.
            :inputs: a list of URLs for datafiles needed as inputs to the
                simulation.
            :command: (optional) the path to the main Python script relative to
                the root of the repository or zip file. Defaults to "run.py {system}".
            :tags: (optional) a list of tags (strings) describing the job.
            :wait: (default False) if True, do not return until the job has completed,
                if False, return immediately with the job id.

        *Returns*:
            The job id as a relative URI
            unless `wait=True`, in which case returns the job as a dictionary.

        *Notes*:
            If the `source` argument is a directory containing Python code, the
            directory contents will be uploaded to Collab storage into a folder
            named according to the property `client.collab_source_folder`
            (default: "source_code")
        """
        job = {
            'command': command,
            'hardware_platform': platform,
            'collab_id': collab_id,
            'user_id': self.user_info["id"]
        }

        source = os.path.expanduser(source)
        if os.path.exists(source):
            if os.path.splitext(source)[1] == ".py":
                with open(source, "r") as fp:
                    job['code'] = fp.read()
            elif os.path.isdir(source):
                remote_folder = self.upload_to_storage(source,
                                                       collab_id,
                                                       remote_folder=self.collab_source_folder,
                                                       overwrite=True)
                job['code'] = remote_folder["uuid"]
                job['selected_tab'] = "upload_script"
                job['command'] = self.collab_source_folder + "/" + job["command"]
        else:
            job['code'] = source

        if inputs is not None:
            job['input_data'] = [self.create_data_item(input) for input in inputs]
        if config is not None:
            job['hardware_config'] = config
        if tags is not None:
            if isinstance(tags, (list, tuple)):
                job["tags"] = tags
            else:
                raise ValueError("Job not submitted: 'tags' field should be a list.")
        logger.debug("Submitting job: {}".format(job))
        job_id = self._post(self.job_server + self.resource_map["queue"], job)
        print("Job submitted")
        if wait:
            time.sleep(self.sleep_interval)
            state = self.job_status(job_id)
            while state not in ('finished', 'error'):
                time.sleep(self.sleep_interval)
                state = self.job_status(job_id)
            result = self.get_job(job_id, with_log=True)
            print("Job {}".format(state))
        else:
            result = job_id
        return result

    def submit_comment(self, job_id, text):
        """
        Submit a comment to a job (results resource) in the platform.

        *Arguments*:
            :job_id: id (integer or URI) of the job the comment will be submitted to.
            :text: the content of the comment.
        """
        status = self.get_job(job_id, with_log=False)["status"]
        if status not in ['finished', 'error']:
            return "Comment not submitted: job id must belong to a completed job (with status finished or error)."

        comment = {
            'content': text,
            'user': self.user_info["id"]
        }

        try:
            job_id = int(job_id)
            comment['job'] = "{}/{}".format(self.resource_map["results"], job_id)
        except ValueError:
            comment['job'] = job_id

        result = self._post(self.job_server + self.resource_map["comment"], comment)
        print("Comment submitted")
        return result

    def job_status(self, job_id):
        """
        Return the current status of the job with ID `job_id` (integer or URI).
        """
        return self.get_job(job_id, with_log=False)["status"]

    def get_job(self, job_id, with_log=True):
        """
        Return full details of the job with ID `job_id` (integer or URI).
        """
        # we accept either an integer job id or a resource uri as identifier
        try:
            job_id = int(job_id)
        except ValueError:
            job_id = int(job_id.split("/")[-1])
        job = None

        # try both "results" and "queue" endpoints to see if the job is there.
        # The order is important to avoid a race condition where the job completes
        # in between the two calls.
        for resource_type in ("queue", "results"):
            job_uri = self.job_server + self.resource_map[resource_type] + "/{}".format(job_id)
            job = self._query(job_uri, ignore404=True)
            if job is not None:
                break

        if job is None:
            raise Exception("No such job: %s" % job_id)  # todo: define custom Exceptions

        assert job["id"] == job_id
        if with_log:
            try:
                log = self._query(self.job_server + self.resource_map['log'] + "/{}".format(job_id))
            except Exception:
                job["log"] = ''
            else:
                assert log["resource_uri"] == '/api/v2/log/{}'.format(job_id)
                job["log"] = log["content"]
        return job

    def remove_completed_job(self, job_id):
        """
        Remove a job from the interface.

        The job is hidden rather than being permanently deleted.
        """
        try:
            job_id = int(job_id)
            job_uri = "{}/{}".format(self.resource_map["results"], job_id)
        except ValueError:
            job_uri = job_id
        self._delete(self.job_server + job_uri)

    def remove_queued_job(self, job_id):
        """
        Remove a job from the interface.

        The job is hidden rather than being permanently deleted.
        """
        try:
            job_id = int(job_id)
            job_uri = "{}/{}".format(self.resource_map["queue"], job_id)
        except ValueError:
            job_uri = job_id
        self._delete(self.job_server + job_uri)

    def queued_jobs(self, verbose=False):
        """
        Return the list of jobs belonging to the current user in the queue.

        *Arguments*:
            :verbose: if False, return just the job URIs,
                      if True, return full details.
        """
        return self._query(self.job_server + self.resource_map["queue"] + "/submitted/?user_id=" + str(self.user_info["id"]), verbose=verbose)

    def completed_jobs(self, collab_id, verbose=False):
        """
        Return the list of completed jobs in the given collab.

        *Arguments*:
            :verbose: if False, return just the job URIs,
                      if True, return full details.
        """
        return self._query(self.job_server + self.resource_map["results"] + "?collab_id=" + str(collab_id),
                           verbose=verbose)

    def download_data(self, job, local_dir=".", include_input_data=False):
        """
        Download output data files produced by a given job to a local directory.

        *Arguments*:
            :job: a full job description (dict), as returned by `get_job()`.
            :local_dir: path to a directory into which files shall be saved.
            :include_input_data: also download input data files.
        """
        filenames = []
        datalist = job["output_data"]
        if include_input_data:
            datalist.extend(job["input_data"])

        if datalist:
            server_paths = [urlparse(item["url"])[2] for item in datalist]
            if len(server_paths) > 1:
                common_prefix = os.path.dirname(os.path.commonprefix(server_paths))
            else:
                common_prefix = os.path.dirname(server_paths[0])
            relative_paths = [os.path.relpath(p, common_prefix) for p in server_paths]

            for relative_path, dataitem in zip(relative_paths, datalist):
                url = dataitem["url"]
                (scheme, netloc, path, params, query, fragment) = urlparse(url)
                if not scheme:
                    url = "file://" + url
                local_path = os.path.join(local_dir, "job_{}".format(job["id"]), relative_path)
                dir = os.path.dirname(local_path)
                _mkdir_p(dir)
                urlretrieve(url, local_path)
                filenames.append(local_path)

        return filenames

    def copy_data_to_storage(self, job_id, destination="collab"):
        """
        Copy the data produced by the job with id `job_id` to Collaboratory
        storage or to the HPAC Platform. Note that copying data to an HPAC
        site requires that you have an account for that site.

        *Example*:

        To copy data to the JURECA machine::

            client.copy_data_to_storage(90712, "JURECA")

        To copy data to Collab storage::

            client.copy_data_to_storage(90712, "collab")

        """
        return self._query(self.job_server + "/copydata/{}/{}".format(destination, job_id))

    def create_data_item(self, url):
        """
        Register a data item with the platform.
        """
        data_item = {"url": url}
        result = self._post(self.job_server + self.resource_map["dataitem"], data_item)
        return result

    def upload_to_storage(self, local_directory, collab_id, remote_folder="",
                          overwrite=False, include=["*.py"]):
        """
        Upload the contents of a local directory to Collab storage.

        This ignores hidden directories (names starting with ".") and only
        uploads files whose names match the patterns in the `include` argument.

        *Arguments*:
            :local_directory: path of the directory to be uploaded.
            :collab_id: the ID of the collab to whose storage the files will be uploaded.
            :remote_folder: relative path of the remote folder in which to put the uploaded files.
            :overwrite: (default False) if True, overwrite files that already exist,
                        otherwise raise a StorageException
            :include: list of wildcard patterns indicating which files should be uploaded.
                      By default, matches only Python files

        *Returns*:
            the entity id of the remote folder
        """
        # todo: add support for Drive
        if not self.storage_client:
            if have_collab_client:
                self.storage_client = StorageClient.new(self.token)
            else:
                raise ImportError("Please install the hbp_service_client package")

        base_path = '/{}'.format(self.storage_client.api_client.list_projects(collab_id=collab_id)['results'][0]['name'])

        uploads = []
        remote_dirs = set()
        for dirpath, dirnames, filenames in os.walk(local_directory):
            # don't enter hidden directories
            for dirname in dirnames:
                if dirname.startswith("."):
                    dirnames.remove(dirname)

            matches = []
            for pattern in include:
                matches.extend(fnmatch.filter(filenames, pattern))
            relative_dir = os.path.relpath(dirpath, local_directory)
            if relative_dir == ".":
                relative_dir = ""
            if matches:
                for filename in matches:
                    local_path = os.path.join(dirpath, filename)
                    remote_dir = os.path.join(base_path, remote_folder, relative_dir).rstrip("/")  # trailing slash not allowed by mkdir
                    remote_dirs.add(remote_dir)
                    remote_path = os.path.join(remote_dir, filename)
                    content_type = mimetypes.guess_type(local_path, strict=False)[0]
                    uploads.append((local_path, remote_path, content_type))

        # Create remote directories as needed
        for remote_path in sorted(remote_dirs, key=lambda x: len(x)):
            # sort to ensure we create parents before children.
            # todo: keep track of directories that already exist to avoid
            #       trying to create them more than once
            path_parts = remote_path.split("/")
            for i in range(3, len(path_parts) + 1):
                rpath = "/".join(path_parts[:i])
                try:
                    self.storage_client.mkdir(rpath)
                except StorageException as err:
                    if "already exists" not in err.args[0]:
                        raise

        # Upload files
        # Keeps track of last modified times for uploaded files
        # to avoid uploading unchanged files
        n = len(uploads)
        errors = []

        upload_cache = {str(collab_id): {remote_folder: {}}}
        if os.path.exists(".hbp_storage"):  # check for record of previous uploads
            with open(".hbp_storage") as fp:
                upload_cache = json.load(fp)
        last_upload_times = upload_cache.get(str(collab_id), {}).get(remote_folder, {})

        for i, (local_path, remote_path, content_type) in enumerate(uploads, start=1):
            last_upload_time = last_upload_times.get(local_path, -1)
            last_modified_time = os.path.getmtime(local_path)
            if last_modified_time > last_upload_time:
                print("[Uploading {} / {}] {} --> {}".format(i, n, local_path, remote_path))
                try:
                    self.storage_client.upload_file(local_path, remote_path, content_type)
                except StorageException as err:
                    if overwrite:
                        self.storage_client.delete(remote_path)
                        self.storage_client.upload_file(local_path, remote_path, content_type)
                    else:
                        errors.append(remote_path)
                upload_cache[str(collab_id)][remote_folder][local_path] = int(time.time())
            else:
                print("Not uploading {}, file unchanged".format(local_path))
        if errors:
            errmsg = "The following files were not uploaded as they already exist: \n  "
            errmsg += "\n  ".join(errors)
            raise StorageException(errmsg)

        # save upload times
        with open(".hbp_storage", "w") as fp:
            json.dump(upload_cache, fp, indent=2)

        return self.storage_client.api_client.get_entity_by_query(path=os.path.join(base_path, remote_folder))

    def my_collabs(self):
        """
        Return a list of collabs of which the user is a member.
        """
        if "roles" in self.user_info:
            return self.user_info["roles"]["team"]
            # todo: retrieve more information, like Collab names
        else:
            collabs = []
            next = COLLAB_SERVICE_V1 + '/mycollabs'
            while next:
                req = requests.get(next, auth=self.auth)
                if req.ok:
                    data = req.json()
                    next = data["next"]
                    collabs.extend(data["results"])
                else:
                    self._handle_error(req)
            return dict((c["title"], c)
                        for c in collabs if not c["deleted"])

    def create_resource_request(self, title, collab_id, abstract, description=None, submit=False):
        """
        Create a new resource request. By default, it will not be submitted.
        """

        context = str(uuid.uuid4())
        try:
            int(collab_id)
            version = 1
        except ValueError:
            version = 2

        if version == 1:
            # create a new nav item in the Collab
            nav_resource = COLLAB_SERVICE_V1 + "/collab/{}/nav/".format(collab_id)
            nav_root = self._query(nav_resource + "root")['id']
            nav_item = {
                "app_id": "206",
                "context": context,
                "name": "Resource request",
                "order_index": "-1",
                "parent": nav_root,
                "type": "IT"
            }
            result = self._post(nav_resource, nav_item)

        # create the resource request
        new_project = {
            'context': context,
            'collab': collab_id,
            'owner': self.user_info['id'],
            'title': title,
            'abstract': abstract,
            'description': description or ''
        }
        if submit:
            new_project["submitted"] = True
        result = self._post(self.quotas_server + "/projects/",
                            new_project)
        if submit:
            print("Resource request {} submitted.".format(result["context"]))
        else:
            print("Resource request {} created. Use `edit_resource_request()` to edit and submit".format(result["context"]))
        return result["resource_uri"]

    def edit_resource_request(self, request_id, title=None, abstract=None, description=None, submit=False):
        """
        Edit and/or submit an unsubmitted resource request
        """
        # todo: support using a URI as the request_id
        resource_uri = self.quotas_server + "/projects/" + request_id
        data = {"submitted": submit}
        if title:  # title cannot be blank
            data["title"] = title
        if abstract is not None:
            data["abstract"] = abstract
        if description is not None:
            data["description"] = description
        result = self._put(resource_uri, data)
        return data

    def list_resource_requests(self, collab_id, status=None):
        """
        Return a list of resource requests for the Neuromorphic Platform
        """
        url = self.quotas_server + "/projects/"
        filters = {}
        if collab_id is not None:
            filters["collab"] = collab_id
        if status is not None:
            filters["status"] = status
        if filters:
            url += "?" + urlencode(filters)
        return self._query(url)

    def list_quotas(self, collab_id):
        """
        Return a list of quotas for running jobs on the Neuromorphic Platform
        """
        resource_requests = self.list_resource_requests(collab_id, status="accepted")
        quotas = []
        for rr in resource_requests:
            quotas.append(self._query(self.quotas_server + rr["resource_uri"] + "/quotas/"))
        return quotas
