"""
process utilities
"""
import shlex
import subprocess
import logging
import rna.log


def execute(system_command, level=logging.DEBUG, **kwargs):
    """
    Execute a system command, passing STDOUT and STDERR to logger.

    Examples:
        >>> import rna
        >>> import logging
        >>> rna.process.execute("echo 'Test'", level=logging.ERROR)

    """
    logging.log(level, "Executing system command: '%s'", system_command)
    popen = subprocess.Popen(
        shlex.split(system_command),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        **kwargs
    )
    rna.log.pipe(popen.stdout)
    popen.stdout.close()
    return_code = popen.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, system_command)
