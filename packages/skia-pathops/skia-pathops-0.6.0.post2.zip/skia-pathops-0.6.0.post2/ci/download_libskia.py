import argparse
import glob
import logging
import platform
import os
import shutil
import struct
import tempfile

__requires__ = ["github_release"]

import github_release


GITHUB_REPO = "fonttools/skia-builder"
ASSET_TEMPLATE = "libskia-{plat}-{arch}.zip"
DOWNLOAD_DIR = os.path.join("build", "download")
CPU_ARCH = "x64" if struct.calcsize("P") * 8 == 64 else "x86"
PLATFORM_TAGS = {"Linux": "linux", "Darwin": "mac", "Windows": "win"}


logger = logging.getLogger()


def get_latest_release(repo):
    releases = github_release.get_releases(repo)
    if not releases:
        raise ValueError("no releases found for {!r}".format(repo))
    return releases[0]


def download_unpack_assets(repo, tag, asset_name, dest_dir):
    dest_dir = os.path.abspath(dest_dir)
    os.makedirs(dest_dir, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmpdir:
        curdir = os.getcwd()
        os.chdir(tmpdir)
        try:
            downloaded = github_release.gh_asset_download(repo, tag, asset_name)
        except:
            raise
        else:
            if not downloaded:
                raise ValueError(
                    "no assets found for {0!r} with name {1!r}".format(tag, asset_name)
                )
            for archive in glob.glob(asset_name):
                shutil.unpack_archive(archive, dest_dir)
        finally:
            os.chdir(curdir)


if __name__ == "__main__":
    logging.basicConfig(level="INFO")

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-p",
        "--platform",
        default=PLATFORM_TAGS.get(platform.system(), "win"),
        choices=["win", "mac", "linux"],
        help="The desired platform (default: %(default)s)",
    )
    parser.add_argument(
        "-a",
        "--cpu-arch",
        default=CPU_ARCH,
        help="The desired CPU architecture (default: %(default)s)",
        choices=["x86", "x64"],
    )
    parser.add_argument(
        "-d",
        "--download-dir",
        default=DOWNLOAD_DIR,
        help="directory where to download libskia (default: %(default)s)",
    )
    parser.add_argument(
        "-t", "--tag-name", default=None, help="release tag name (default: latest)"
    )
    args = parser.parse_args()

    tag_name = args.tag_name
    if tag_name is None:
        latest_release = get_latest_release(GITHUB_REPO)
        tag_name = latest_release["tag_name"]

    asset_name = ASSET_TEMPLATE.format(plat=args.platform, arch=args.cpu_arch)

    logger.info(
        "Downloading '%s' from '%s' at tag '%s' to %s",
        asset_name,
        GITHUB_REPO,
        tag_name,
        args.download_dir,
    )
    download_unpack_assets(GITHUB_REPO, tag_name, asset_name, args.download_dir)
