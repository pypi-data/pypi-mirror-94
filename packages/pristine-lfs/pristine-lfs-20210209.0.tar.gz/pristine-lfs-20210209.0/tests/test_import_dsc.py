from textwrap import dedent

from pristine_lfs import do_import, do_list


def test_pristine_lfs_import_dsc(fake_tarball, capsys):
    repo, tarball, size, sha = fake_tarball

    base, *_ = tarball.name.split('.')
    package, version = base.split('_')

    outdir = repo / 'tmp'
    outdir.mkdir()
    dsc = outdir / f'{package}_{version}.dsc'
    dsc.write_text(dedent(
        f"""
        Format: 3.0 (quilt)
        Source: {package}
        Binary: {package}
        Architecture: any
        Version: {version}
        Package-List:
         {package} deb utils optional arch=any
        Checksums-Sha1:
         0000000000000000000000000000000000000000 0 {tarball.name}
        Checksums-Sha256:
         0000000000000000000000000000000000000000000000000000000000000000 0 {tarball.name}
        Files:
         00000000000000000000000000000000 0 {tarball.name}
        """).lstrip('\n'))

    tarball.rename(outdir / tarball.name)

    do_import(dsc.open(), 'pristine-lfs', f'import {package}')
    do_import(dsc.open(), 'pristine-lfs', f'import {package}')
    do_import(dsc.open(), 'pristine-lfs-source', f'import {package}', full=True)

    do_list(branch='pristine-lfs')
    captured = capsys.readouterr()
    assert ['true_0.orig.tar.gz'] == captured.out.splitlines()

    do_list(branch='pristine-lfs-source')
    captured = capsys.readouterr()
    assert ['true_0.dsc', 'true_0.orig.tar.gz'] == captured.out.splitlines()

