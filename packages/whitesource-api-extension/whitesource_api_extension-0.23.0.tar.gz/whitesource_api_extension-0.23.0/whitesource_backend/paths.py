import os
import shutil

wss_agent_dir = '/tmp'
wss_agent_name = 'wss_unified_agent.jar'
wss_agent_path = os.path.join(wss_agent_dir, wss_agent_name)
java_path = shutil.which(cmd='java')
static_config_path = '../whitesource-fs-agent.config' # noqa E501
