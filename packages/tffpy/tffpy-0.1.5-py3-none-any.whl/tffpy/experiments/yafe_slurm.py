# -*- coding: utf-8 -*-
# ######### COPYRIGHT #########
# Credits
# #######
#
# Copyright(c) 2020-2020
# ----------------------
#
# * Laboratoire d'Informatique et Systèmes <http://www.lis-lab.fr/>
# * Université d'Aix-Marseille <http://www.univ-amu.fr/>
# * Centre National de la Recherche Scientifique <http://www.cnrs.fr/>
# * Université de Toulon <http://www.univ-tln.fr/>
#
# Contributors
# ------------
#
# * `Valentin Emiya <mailto:valentin.emiya@lis-lab.fr>`_
# * `Ama Marina Krémé <mailto:ama-marina.kreme@lis-lab.fr>`_
#
# This package has been created thanks to the joint work with Florent Jaillet
# and Ronan Hamon on other packages.
#
# Description
# -----------
#
# Time frequency fading using Gabor multipliers
#
# Version
# -------
#
# * tffpy version = 0.1.4
#
# Licence
# -------
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# ######### COPYRIGHT #########
"""

.. moduleauthor:: Valentin Emiya
"""

import importlib
import os
from pathlib import Path
import stat
import sys


def generate_slurm_script(script_file_path, xp_var_name, task_ids=None,
                          n_simultaneous_jobs=10, slurm_walltime='02:00:00',
                          activate_env_command=None, use_cpu_gpu='cpu'):
    """Generate a script to launch an experiment using Slurm.

    Tasks are divided into batches that are executed by oar jobs.

    The resulting script is written in the experiment folder, and the command
    to launch the jobs with Slurm is displayed in the terminal.

    An example of a similar usage in the case of OAR (script
    :func:`yafe.utils.generate_oar_script`) is illustrated by in
    :ref:`tutorial <tutorial_oar>`.

    Parameters
    ----------
    script_file_path : str
        File path to the script that defines the experiment.
    xp_var_name : str
        Name of the variable containing the experiment in the script.
    task_ids : list
        List of tasks ids to run.
        If ``task_ids`` is ``None``, the list of pending tasks of the
        experiment is used.
    batch_size : int
        Number of tasks run in each batch.
    slurm_walltime : str
        Wall time for each Slurm job ('HH:MM:SS').
    activate_env_command : str or None
        Optional command that must be run to activate a Python virtual
        environment before launching the experiment.
        Typically, this is a command of the form
        ``source some_virtual_env/bin/activate`` when using virtualenv and
        ``source activate some_conda_env`` when using conda.
        If ``activate_env_command`` is ``None``, no virtual environment is
        activated.
    use_cpu_gpu : {'all', 'cpu', 'gpu'}
        Parameter to choose using CPU, GPU or both.
    """
    script_file_path = Path(script_file_path)
    script_dir = script_file_path.parent
    script_name = script_file_path.stem

    sys.path.append(str(script_dir))
    mod = importlib.import_module(script_name)
    xp = getattr(mod, xp_var_name)
    script_dir = xp.xp_path / 'job_scripts'
    script_dir.mkdir(exist_ok=True)
    for f in script_dir.glob('*.sh'):
        os.remove(f)

    if task_ids is None:
        task_ids = xp.get_pending_task_ids()

    # generate and save script

    # Generate job script
    log_dir = xp.xp_path / 'logs'
    log_dir.mkdir(exist_ok=True)
    script = '#!/bin/sh\n'
    # define parameters
    script += '#SBATCH --job-name={}\n'.format(xp.name)
    script += '#SBATCH --array={}%{}\n'.format(
        ','.join(str(i) for i in task_ids), n_simultaneous_jobs)
    script += '#SBATCH --output={}/stdout_%A_%a.slurm\n'.format(log_dir)
    script += '#SBATCH --error={}/stderr_%A_%a.slurm\n'.format(log_dir)
    script += '#SBATCH --time={}\n'.format(slurm_walltime)
    if use_cpu_gpu in ('cpu', 'gpu'):
        script += '#SBATCH --partition={}\n'.format(use_cpu_gpu)

    script += 'srun -N1 -n1 {}/run_$SLURM_ARRAY_TASK_ID.sh'.format(script_dir)

    script_path = script_dir / 'script_slurm.sh'
    with script_path.open('w') as file:
        file.write(script)
    status = os.stat(script_path)
    os.chmod(script_path, status.st_mode | stat.S_IXUSR)

    # Generate a script of each array element
    for idt in task_ids:
        script = '#!/bin/sh\n'

        # activate the virtual env
        if activate_env_command is not None and len(activate_env_command) > 0:
            script += '{}\n'.format(activate_env_command)

        # python command
        script += 'echo "Running {}.launch_experiment(task_ids=[{}])"\n'\
            .format(xp_var_name, idt)
        script += 'python -c "import sys; sys.path.append(\'{0}\'); ' \
            'from {1} import {2}; ' \
            '{2}.launch_experiment(task_ids=[{3}])"\n'.format(
                script_dir, script_name, xp_var_name, idt)
        script += 'exit $?'

        script_i_path = script_dir / 'run_{}.sh'.format(idt)
        with script_i_path.open('w') as file:
            file.write(script)
        status = os.stat(script_i_path)
        os.chmod(script_i_path, status.st_mode | stat.S_IXUSR)

    print('*' * 80)
    print('Submit the job array using:')
    print('sbatch {}'.format(str(script_path)))
    print('*' * 80)
