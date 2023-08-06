import pytest


def test_without(testdir):
    testdir.makepyfile(
        """
        def test_01():
            a = 5
            b = 10
            assert a + b == 15
        def test_02():
            a = 10
            b = 5
            assert a + b != 15
        """
    )
    result = testdir.runpytest()
    result.assert_outcomes(passed=1, failed=1)


def test_help(testdir):
    testdir.makepyfile(
        """
        def test_01():
            a = "pytest"
            b = "py"
            assert a == b
        """
    )
    result = testdir.runpytest("--help")
    result.stdout.fnmatch_lines(["*--concurrent*"])
    result.stdout.fnmatch_lines(["*--sub_group=*"])


def test_on(testdir):
    testdir.makepyfile(
        """
        import pytest
        @pytest.mark.parametrize("group", ["group_1", "group_2", "group_3"])
        def test_01(group):
            a = "hello world"
            b = "hello world"
            assert a == b
            
        def test_02():
            a = "hello"
            b = "world"
            assert a == b
        """
    )
    result = testdir.runpytest("-svv", "--concurrent=on")
    result.assert_outcomes(passed=3, failed=1)


def test_on_group_none_param(testdir):
    testdir.makepyfile(
        """
        def test_01():
            a = "hello world"
            b = "hello world"
            assert a == b

        def test_02():
            a = "hello"
            b = "world"
            assert a == b
        """
    )
    result = testdir.runpytest("--concurrent=on", "--sub_group=name")
    result.assert_outcomes(passed=1, failed=1)


def test_on_group_have_param(testdir):
    testdir.makepyfile(
        """
        import pytest
        @pytest.mark.parametrize("name", ["group_1", "group_2", "group_3"])
        def test_01(name):
            a = "hello world"
            b = "hello world"
            assert a == b

        @pytest.mark.parametrize("name", ["group_1", "group_2", "group_3"])
        def test_02(name):
            a = "hello"
            b = "world"
            assert a == b

        @pytest.mark.parametrize("name", ["group_1", "group_2", "group_3"])
        def test_03(name):
            a = "hello"
            b = "world"
            assert a == b

        @pytest.mark.parametrize("name", ["group_1", "group_2", "group_3"])
        def test_04(name):
            a = "hello"
            b = "world"
            assert a == b

        @pytest.mark.parametrize("name", ["group_1", "group_2", "group_3"])
        def test_05(name):
            a = "hello"
            b = "world"
            assert a == b
        """
    )
    result = testdir.runpytest("-svv", "--concurrent=on", "--sub_group=name")
    result.assert_outcomes(passed=3, failed=12)


def test_off(testdir):
    testdir.makepyfile(
        """
        def test_01():
            a = "hello world"
            b = "hello world"
            assert a == b

        def test_02():
            a = "hello"
            b = "world"
            assert a == b
        """
    )
    result = testdir.runpytest("--concurrent=off")
    result.assert_outcomes(passed=1, failed=1)


def test_off_group(testdir):
    testdir.makepyfile(
        """
        import pytest
        @pytest.mark.parametrize("group_by", ["group_1", "group_2", "group_3"])
        def test_01(group_by):
            a = "hello world"
            b = "hello world"
            assert a == b

        def test_02():
            a = "hello"
            b = "world"
            assert a == b
        """
    )
    result = testdir.runpytest("--concurrent=off", "--sub_group=group_by")
    result.assert_outcomes(passed=3, failed=1)


def test_off_group_have_param(testdir):
    testdir.makepyfile(
        """
        import pytest
        @pytest.mark.parametrize("name", ["group_1", "group_2", "group_3"])
        def test_01(name):
            a = "hello world"
            b = "hello world"
            assert a == b

        @pytest.mark.parametrize("name", ["group_1", "group_2", "group_3"])
        def test_02(name):
            a = "hello"
            b = "world"
            assert a == b

        @pytest.mark.parametrize("name", ["group_1", "group_2", "group_3"])
        def test_03(name):
            a = "hello"
            b = "world"
            assert a == b

        @pytest.mark.parametrize("name", ["group_1", "group_2", "group_3"])
        def test_04(name):
            a = "hello"
            b = "world"
            assert a == b

        @pytest.mark.parametrize("name", ["group_1", "group_2", "group_3"])
        def test_05(name):
            a = "hello"
            b = "world"
            assert a == b
        """
    )
    result = testdir.runpytest("--concurrent=off", "--sub_group=name")
    result.assert_outcomes(passed=3, failed=12)


if __name__ == '__main__':
    # pytest.main(["--concurrent=on"])
    # pytest.main(["-svv"])
    pytest.main(["-sv", "test_plugin.py::test_on_group_have_param"])
