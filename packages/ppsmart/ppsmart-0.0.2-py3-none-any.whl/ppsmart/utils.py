import pkg_resources
from typing import List


def list_installed_packages() -> List:
    installed_packages = pkg_resources.working_set
    installed_packages_list = sorted(["%s==%s" % (i.key, i.version) for i in installed_packages])
    print(installed_packages_list)
    return installed_packages_list


def seed_everything(seed_number: int):
    print(f"""
    np.random.seed({seed_number})
    random.seed({seed_number})
    os.environ['PYTHONHASHSEED'] = str({seed_number})
    torch.backends.cudnn.benchmark = False
    torch.backends.cudnn.deterministic = True
    torch.manual_seed({seed_number})
    torch.cuda.manual_seed({seed_number})
    torch.cuda.manual_seed_all({seed_number})
    """)
