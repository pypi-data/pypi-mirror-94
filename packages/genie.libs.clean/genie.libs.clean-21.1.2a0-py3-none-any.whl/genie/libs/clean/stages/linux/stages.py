
from genie.libs.clean.utils import clean_schema

from pyats import aetest

@clean_schema({
    'commands': list
})
@aetest.test
def execute_command(section, steps, device, commands):
    try:
        device.execute(commands)
    except Exception as e:
        section.failed("configuration failed. Error: {}".format(e))

