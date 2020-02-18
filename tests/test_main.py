import Main


class TestMain(object):
    def test_run(self, capfd):
        Main.run("HelloWorld")

        out, err = capfd.readouterr()
        assert out == "Hello World!!\n"
        assert err is ''
