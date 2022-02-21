from typing import Optional

from hikari import (
    UNDEFINED,
    ChannelType,
    CommandOption,
    CommandType,
    Message,
    OptionType,
    PartialChannel,
    User,
)
from typing_extensions import Annotated

from crescent import Context, Name, command, message_command, user_command
from crescent.commands.args import ChannelTypes, MaxValue, MinValue
from crescent.internal.app_command import AppCommand, AppCommandMeta


class TestCommandFunction:
    def test_slash_command(self):
        @command(name="test", description="1234", guild=12345678)
        async def callback(ctx: Context):
            pass

        assert callback.metadata == AppCommandMeta(
            app=AppCommand(
                type=CommandType.SLASH,
                name="test",
                guild_id=12345678,
                default_permission=UNDEFINED,
                description="1234",
            )
        )

    def test_annotated_command(self):
        @command(description="1234")
        async def callback(
            ctx: Context,
            arg_1: Annotated[str, "1234"],
            arg_2: Annotated[Optional[str], "1234"] = None,
            arg_3: Optional[float] = None,
        ):
            pass

        assert callback.metadata == AppCommandMeta(
            app=AppCommand(
                type=CommandType.SLASH,
                name="callback",
                guild_id=None,
                default_permission=UNDEFINED,
                description="1234",
                options=[
                    CommandOption(
                        type=OptionType.STRING, name="arg_1", description="1234", is_required=True
                    ),
                    CommandOption(
                        type=OptionType.STRING, name="arg_2", description="1234", is_required=False
                    ),
                    CommandOption(
                        type=OptionType.FLOAT,
                        name="arg_3",
                        description="No Description",
                        is_required=False,
                    ),
                ],
            )
        )

    def test_crescent_annotations(self):
        @command(description="1234")
        async def callback(
            ctx: Context,
            test_name: Annotated[str, "1234", Name("name_override")],
            test_min_and_max: Annotated[int, "1234", MinValue(0), MaxValue(10)] = None,
            test_channels: Annotated[
                PartialChannel, "1234", ChannelTypes(ChannelType.GUILD_TEXT)
            ] = None,
        ):
            pass

        print(callback.metadata.app.options[2].channel_types)

        assert callback.metadata == AppCommandMeta(
            app=AppCommand(
                type=CommandType.SLASH,
                name="callback",
                default_permission=UNDEFINED,
                description="1234",
                guild_id=None,
                options=[
                    CommandOption(
                        type=OptionType.STRING,
                        name="name_override",
                        description="1234",
                        is_required=True,
                    ),
                    CommandOption(
                        type=OptionType.INTEGER,
                        name="test_min_and_max",
                        description="1234",
                        is_required=False,
                        min_value=0,
                        max_value=10,
                    ),
                    CommandOption(
                        type=OptionType.CHANNEL,
                        name="test_channels",
                        description="1234",
                        is_required=False,
                        channel_types=[ChannelType.GUILD_TEXT],
                    ),
                ],
            )
        )

    def test_message_command(self):
        @message_command
        async def callback(ctx: Context, message: Message):
            pass

        assert callback.metadata == AppCommandMeta(
            app=AppCommand(
                type=CommandType.MESSAGE,
                name="callback",
                default_permission=UNDEFINED,
                guild_id=None,
            )
        )

    def test_user_command(self):
        @user_command
        async def callback(ctx: Context, user: User):
            pass

        assert callback.metadata == AppCommandMeta(
            app=AppCommand(
                type=CommandType.USER, name="callback", default_permission=UNDEFINED, guild_id=None
            )
        )
