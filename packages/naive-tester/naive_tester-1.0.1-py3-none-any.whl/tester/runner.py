"""Run an external script and assess its output"""
import sys
import subprocess
import logging

logger = logging.getLogger(__name__)


def run_job(job):
    """Run a script with it's arguments.

    Parameters
    ----------
    job : a tuple of script's name and it's arguments.

    Returns
    --------
    Standard out of a script in a string form.

    """
    script, args = job
    output = subprocess.run(
        [sys.executable] + [script, args],
        stdout=subprocess.PIPE,
        universal_newlines=True).stdout.strip('\n')
    return output


def assert_job(job, reference_output):
    """Check if script's output coincides with the reference output."""
    script, args = job
    try:
        assert run_job(job) == reference_output
        logger.info(f'Successfully run the {script} with {args}')
    except AssertionError:
        logger.error(
            f'Failed run of the {script} with {args}. '
            f'The output should be {reference_output}.')


def run_jobs(jobs_with_outputs):
    """Sequentially run scripts."""
    for job_with_output in jobs_with_outputs:
        assert_job(*job_with_output)
