# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=line-too-long
import contextlib
import io
import os
import tempfile
import logging

import pytest
import machine
import translator


@pytest.mark.golden_test("tests/golden/hello.yml")
def test_hello_program(golden, caplog):
    caplog.set_level(logging.DEBUG)

    with tempfile.TemporaryDirectory() as tmp_dir_name:
        source = os.path.join(tmp_dir_name, "hello.txt")
        target = os.path.join(tmp_dir_name, "hello.bin")
        mnem = os.path.join(tmp_dir_name, "hello.out.mnem")
        input = os.path.join(tmp_dir_name, "input.txt")

        with open(source, "w", encoding="utf-8") as file:
            file.write(golden["source"])

        with open(input, "w", encoding="utf-8") as file:
            file.write(golden.get("input", ""))

        with contextlib.redirect_stdout(io.StringIO()) as stdout:
            translator.main([source, mnem, target])
            machine.main([target, input])

        with open(target, "rb") as file:
            code = file.read().hex()

        with open(mnem, "r", encoding="utf-8") as file:
            mnemonics = file.read()

        assert mnemonics == golden.out["out_mnemonics"]
        assert code == golden.out["code"]
        assert stdout.getvalue() == golden.out["output"]
        assert caplog.text == golden["log"]


@pytest.mark.golden_test("tests/golden/cat.yml")
def test_cat_program(golden, caplog):
    caplog.set_level(logging.DEBUG)

    with tempfile.TemporaryDirectory() as tmp_dir_name:
        source = os.path.join(tmp_dir_name, "cat.txt")
        mnem = os.path.join(tmp_dir_name, "cat.out.mnem")
        target = os.path.join(tmp_dir_name, "cat.bin")
        input = os.path.join(tmp_dir_name, "input.txt")

        with open(source, "w", encoding="utf-8") as file:
            file.write(golden["source"])
        with open(input, "w", encoding="utf-8") as file:
            file.write(golden.get("input", ""))

        with contextlib.redirect_stdout(io.StringIO()) as stdout:
            translator.main([source, mnem, target])
            machine.main([target, input])

        with open(target, "rb") as file:
            code = file.read().hex() + "\n"

        with open(mnem, "r", encoding="utf-8") as file:
            mnemonics = file.read()

        assert mnemonics == golden.out["out_mnemonics"]
        assert code == golden.out["code"]
        assert stdout.getvalue() == golden.out["output"]
        assert caplog.text == golden["log"]


@pytest.mark.golden_test("tests/golden/hello_user.yml")
def test_hello_user_program(golden, caplog):
    caplog.set_level(logging.DEBUG)

    with tempfile.TemporaryDirectory() as tmp_dir_name:
        source = os.path.join(tmp_dir_name, "hello_user.txt")
        mnem = os.path.join(tmp_dir_name, "hello_user.out.mnem")
        target = os.path.join(tmp_dir_name, "hello_user.bin")
        input = os.path.join(tmp_dir_name, "input.txt")

        with open(source, "w", encoding="utf-8") as file:
            file.write(golden["source"])
        with open(input, "w", encoding="utf-8") as file:
            file.write(golden.get("input", ""))

        with contextlib.redirect_stdout(io.StringIO()) as stdout:
            translator.main([source, mnem, target])
            machine.main([target, input])

        with open(target, "rb") as file:
            code = file.read().hex()

        with open(mnem, "r", encoding="utf-8") as file:
            mnemonics = file.read()

        assert mnemonics == golden.out["out_mnemonics"]
        assert code == golden.out["code"]
        assert stdout.getvalue() == golden.out["output"]
        assert caplog.text == golden["log"]


@pytest.mark.golden_test("tests/golden/prob1.yml")
def test_prob1_program(golden):
    with tempfile.TemporaryDirectory() as tmp_dir_name:
        source = os.path.join(tmp_dir_name, "prob1.txt")
        mnem = os.path.join(tmp_dir_name, "prob1.out.mnem")
        target = os.path.join(tmp_dir_name, "prob1.bin")
        input = os.path.join(tmp_dir_name, "input.txt")

        with open(source, "w", encoding="utf-8") as file:
            file.write(golden["source"])

        with open(input, "w", encoding="utf-8") as file:
            file.write(golden.get("input", ""))

        with contextlib.redirect_stdout(io.StringIO()) as stdout:
            translator.main([source, mnem, target])
            machine.main([target, input])

        with open(target, "rb") as file:
            code = file.read().hex() + "\n"

        with open(mnem, encoding="utf-8") as file:
            mnemonics = file.read()

        assert mnemonics == golden.out["out_mnemonics"]
        assert code == golden.out["code"]
        assert stdout.getvalue() == golden.out["output"]
