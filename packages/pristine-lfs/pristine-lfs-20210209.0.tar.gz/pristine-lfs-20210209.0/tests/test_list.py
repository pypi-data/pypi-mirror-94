from pristine_lfs import do_list


def test_pristine_lfs_list(test_git_repo, capsys):
    do_list(branch='pristine-lfs')
    captured = capsys.readouterr()
    assert test_git_repo.tarball.name == captured.out.strip('\n'), 'Expected tarball not found'

    do_list(branch='debian/test')
    captured = capsys.readouterr()
    assert "debian/changelog" == captured.out.strip('\n'), 'This branch should only have the changelog'
