from ._omp_wrapper import get_thread_count


__author__ = 'Rolando Espinoza'
__email__ = 'rolando at rmax.io'
__version__ = '0.2.0'


def get_includes():
    """Returns includes directories."""
    import omp_thread_count, os
    mod_dir = os.path.abspath(
        os.path.dirname(omp_thread_count.__file__)
    )
    inc_dir = os.path.join(mod_dir, 'include')
    return [mod_dir, inc_dir]
