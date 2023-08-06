import sys

import pytest

import asyncclick as click
from asyncclick.core import Argument
from asyncclick.core import Command
from asyncclick.core import Group
from asyncclick.core import Option
from asyncclick.shell_completion import CompletionItem
from asyncclick.shell_completion import ShellComplete
from asyncclick.types import Choice
from asyncclick.types import File
from asyncclick.types import Path


async def _get_completions(cli, args, incomplete):
    comp = ShellComplete(cli, {}, cli.name, "_CLICK_COMPLETE")
    return await comp.get_completions(args, incomplete)


async def _get_words(cli, args, incomplete):
    return [c.value for c in await _get_completions(cli, args, incomplete)]


@pytest.mark.anyio
async def test_command():
    cli = Command("cli", params=[Option(["-t", "--test"])])
    assert (await _get_words(cli, [], "")) == []
    assert (await _get_words(cli, [], "-")) == ["-t", "--test", "--help"]
    assert (await _get_words(cli, [], "--")) == ["--test", "--help"]
    assert (await _get_words(cli, [], "--t")) == ["--test"]
    # -t has been seen, so --test isn't suggested
    assert (await _get_words(cli, ["-t", "a"], "-")) == ["--help"]


@pytest.mark.anyio
async def test_group():
    cli = Group("cli", params=[Option(["-a"])], commands=[Command("x"), Command("y")])
    assert (await _get_words(cli, [], "")) == ["x", "y"]
    assert (await _get_words(cli, [], "-")) == ["-a", "--help"]


@pytest.mark.anyio
async def test_group_command_same_option():
    cli = Group(
        "cli", params=[Option(["-a"])], commands=[Command("x", params=[Option(["-a"])])]
    )
    assert (await _get_words(cli, [], "-")) == ["-a", "--help"]
    assert (await _get_words(cli, ["-a", "a"], "-")) == ["--help"]
    assert (await _get_words(cli, ["-a", "a", "x"], "-")) == ["-a", "--help"]
    assert (await _get_words(cli, ["-a", "a", "x", "-a", "a"], "-")) == ["--help"]


@pytest.mark.anyio
async def test_chained():
    cli = Group(
        "cli",
        chain=True,
        commands=[
            Command("set", params=[Option(["-y"])]),
            Command("start"),
            Group("get", commands=[Command("full")]),
        ],
    )
    assert (await _get_words(cli, [], "")) == ["get", "set", "start"]
    assert (await _get_words(cli, [], "s")) == ["set", "start"]
    assert (await _get_words(cli, ["set", "start"], "")) == ["get"]
    # subcommands and parent subcommands
    assert (await _get_words(cli, ["get"], "")) == ["full", "set", "start"]
    assert (await _get_words(cli, ["get", "full"], "")) == ["set", "start"]
    assert (await _get_words(cli, ["get"], "s")) == ["set", "start"]


@pytest.mark.anyio
async def test_help_option():
    cli = Group("cli", commands=[Command("with"), Command("no", add_help_option=False)])
    assert (await _get_words(cli, ["with"], "--")) == ["--help"]
    assert (await _get_words(cli, ["no"], "--")) == []


@pytest.mark.anyio
async def test_argument_order():
    cli = Command(
        "cli",
        params=[
            Argument(["plain"]),
            Argument(["c1"], type=Choice(["a1", "a2", "b"])),
            Argument(["c2"], type=Choice(["c1", "c2", "d"])),
        ],
    )
    # first argument has no completions
    assert (await _get_words(cli, [], "")) == []
    assert (await _get_words(cli, [], "a")) == []
    # first argument filled, now completion can happen
    assert (await _get_words(cli, ["x"], "a")) == ["a1", "a2"]
    assert (await _get_words(cli, ["x", "b"], "d")) == ["d"]


@pytest.mark.anyio
async def test_argument_default():
    cli = Command(
        "cli",
        add_help_option=False,
        params=[
            Argument(["a"], type=Choice(["a"]), default="a"),
            Argument(["b"], type=Choice(["b"]), default="b"),
        ],
    )
    assert (await _get_words(cli, [], "")) == ["a"]
    assert (await _get_words(cli, ["a"], "b")) == ["b"]
    # ignore type validation
    assert (await _get_words(cli, ["x"], "b")) == ["b"]


@pytest.mark.anyio
async def test_type_choice():
    cli = Command("cli", params=[Option(["-c"], type=Choice(["a1", "a2", "b"]))])
    assert (await _get_words(cli, ["-c"], "")) == ["a1", "a2", "b"]
    assert (await _get_words(cli, ["-c"], "a")) == ["a1", "a2"]
    assert (await _get_words(cli, ["-c"], "a2")) == ["a2"]


@pytest.mark.parametrize(
    ("type", "expect"),
    [(File(), "file"), (Path(), "file"), (Path(file_okay=False), "dir")],
)
@pytest.mark.anyio
async def test_path_types(type, expect):
    cli = Command("cli", params=[Option(["-f"], type=type)])
    out = await _get_completions(cli, ["-f"], "ab")
    assert len(out) == 1
    c = out[0]
    assert c.value == "ab"
    assert c.type == expect


@pytest.mark.anyio
async def test_option_flag():
    cli = Command(
        "cli",
        add_help_option=False,
        params=[
            Option(["--on/--off"]),
            Argument(["a"], type=Choice(["a1", "a2", "b"])),
        ],
    )
    assert (await _get_words(cli, [], "--")) == ["--on", "--off"]
    # flag option doesn't take value, use choice argument
    assert (await _get_words(cli, ["--on"], "a")) == ["a1", "a2"]


@pytest.mark.anyio
async def test_option_custom():
    def custom(ctx, param, incomplete):
        return [incomplete.upper()]

    cli = Command(
        "cli",
        params=[
            Argument(["x"]),
            Argument(["y"]),
            Argument(["z"], shell_complete=custom),
        ],
    )
    assert (await _get_words(cli, ["a", "b"], "")) == [""]
    assert (await _get_words(cli, ["a", "b"], "c")) == ["C"]


@pytest.mark.anyio
async def test_autocompletion_deprecated():
    # old function takes args and not param, returns all values, can mix
    # strings and tuples
    def custom(ctx, args, incomplete):
        assert isinstance(args, list)
        return [("art", "x"), "bat", "cat"]

    with pytest.deprecated_call():
        cli = Command("cli", params=[Argument(["x"], autocompletion=custom)])

    assert (await _get_words(cli, [], "")) == ["art", "bat", "cat"]
    assert (await _get_words(cli, [], "c")) == ["cat"]


@pytest.mark.anyio
async def test_option_multiple():
    cli = Command(
        "type",
        params=[Option(["-m"], type=Choice(["a", "b"]), multiple=True), Option(["-f"])],
    )
    assert (await _get_words(cli, ["-m"], "")) == ["a", "b"]
    assert "-m" in await _get_words(cli, ["-m", "a"], "-")
    assert (await _get_words(cli, ["-m", "a", "-m"], "")) == ["a", "b"]
    # used single options aren't suggested again
    assert "-c" not in await _get_words(cli, ["-c", "f"], "-")


@pytest.mark.anyio
async def test_option_nargs():
    cli = Command("cli", params=[Option(["-c"], type=Choice(["a", "b"]), nargs=2)])
    assert (await _get_words(cli, ["-c"], "")) == ["a", "b"]
    assert (await _get_words(cli, ["-c", "a"], "")) == ["a", "b"]
    assert (await _get_words(cli, ["-c", "a", "b"], "")) == []


@pytest.mark.anyio
async def test_argument_nargs():
    cli = Command(
        "cli",
        params=[
            Argument(["x"], type=Choice(["a", "b"]), nargs=2),
            Argument(["y"], type=Choice(["c", "d"]), nargs=-1),
            Option(["-z"]),
        ],
    )
    assert (await _get_words(cli, [], "")) == ["a", "b"]
    assert (await _get_words(cli, ["a"], "")) == ["a", "b"]
    assert (await _get_words(cli, ["a", "b"], "")) == ["c", "d"]
    assert (await _get_words(cli, ["a", "b", "c"], "")) == ["c", "d"]
    assert (await _get_words(cli, ["a", "b", "c", "d"], "")) == ["c", "d"]
    assert (await _get_words(cli, ["a", "-z", "1"], "")) == ["a", "b"]
    assert (await _get_words(cli, ["a", "-z", "1", "b"], "")) == ["c", "d"]


@pytest.mark.anyio
async def test_double_dash():
    cli = Command(
        "cli",
        add_help_option=False,
        params=[
            Option(["--opt"]),
            Argument(["name"], type=Choice(["name", "--", "-o", "--opt"])),
        ],
    )
    assert (await _get_words(cli, [], "-")) == ["--opt"]
    assert (await _get_words(cli, ["value"], "-")) == ["--opt"]
    assert (await _get_words(cli, [], "")) == ["name", "--", "-o", "--opt"]
    assert (await _get_words(cli, ["--"], "")) == ["name", "--", "-o", "--opt"]


@pytest.mark.anyio
async def test_hidden():
    cli = Group(
        "cli",
        commands=[
            Command(
                "hidden",
                add_help_option=False,
                hidden=True,
                params=[
                    Option(["-a"]),
                    Option(["-b"], type=Choice(["a", "b"]), hidden=True),
                ],
            )
        ],
    )
    assert "hidden" not in await _get_words(cli, [], "")
    assert "hidden" not in await _get_words(cli, [], "hidden")
    assert (await _get_words(cli, ["hidden"], "-")) == ["-a"]
    assert (await _get_words(cli, ["hidden", "-b"], "")) == ["a", "b"]


@pytest.mark.anyio
async def test_add_different_name():
    cli = Group("cli", commands={"renamed": Command("original")})
    words = await _get_words(cli, [], "")
    assert "renamed" in words
    assert "original" not in words


def test_completion_item_data():
    c = CompletionItem("test", a=1)
    assert c.a == 1
    assert c.b is None


@pytest.fixture()
def _patch_for_completion(monkeypatch):
    monkeypatch.setattr("asyncclick.core._fast_exit", sys.exit)
    monkeypatch.setattr(
        "asyncclick.shell_completion.BashComplete._check_version", lambda self: True
    )


@pytest.mark.parametrize(
    "shell", ["bash", "zsh", "fish"],
)
@pytest.mark.usefixtures("_patch_for_completion")
def test_full_source(runner, shell):
    cli = Group("cli", commands=[Command("a"), Command("b")])
    result = runner.invoke(cli, env={"_CLI_COMPLETE": f"{shell}_source"})
    assert f"_CLI_COMPLETE={shell}_complete" in result.output


@pytest.mark.parametrize(
    ("shell", "env", "expect"),
    [
        ("bash", {"COMP_WORDS": "", "COMP_CWORD": "0"}, "plain,a\nplain,b\n"),
        ("bash", {"COMP_WORDS": "a b", "COMP_CWORD": "1"}, "plain,b\n"),
        ("zsh", {"COMP_WORDS": "", "COMP_CWORD": "0"}, "plain\na\n_\nplain\nb\nbee\n"),
        ("zsh", {"COMP_WORDS": "a b", "COMP_CWORD": "1"}, "plain\nb\nbee\n"),
        ("fish", {"COMP_WORDS": "", "COMP_CWORD": ""}, "plain,a\nplain,b\tbee\n"),
        ("fish", {"COMP_WORDS": "a b", "COMP_CWORD": "b"}, "plain,b\tbee\n"),
    ],
)
@pytest.mark.usefixtures("_patch_for_completion")
def test_full_complete(runner, shell, env, expect):
    cli = Group("cli", commands=[Command("a"), Command("b", help="bee")])
    env["_CLI_COMPLETE"] = f"{shell}_complete"
    result = runner.invoke(cli, env=env)
    assert result.output == expect


@pytest.mark.usefixtures("_patch_for_completion")
def test_context_settings(runner):
    def complete(ctx, param, incomplete):
        return ctx.obj["choices"]

    cli = Command("cli", params=[Argument("x", shell_complete=complete)])
    result = runner.invoke(
        cli,
        obj={"choices": ["a", "b"]},
        env={"COMP_WORDS": "", "COMP_CWORD": "0", "_CLI_COMPLETE": "bash_complete"},
    )
    assert result.output == "plain,a\nplain,b\n"


@pytest.mark.parametrize(("value", "expect"), [(False, ["Au", "al"]), (True, ["al"])])
@pytest.mark.anyio
async def test_choice_case_sensitive(value, expect):
    cli = Command(
        "cli",
        params=[Option(["-a"], type=Choice(["Au", "al", "Bc"], case_sensitive=value))],
    )
    completions = await _get_words(cli, ["-a"], "a")
    assert completions == expect
