"""
LICENSE
The MIT License (MIT)

Copyright (c) 2020-2021 Skelmis

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
LICENSE
"""
import logging
from copy import deepcopy
from unittest.mock import MagicMock

import discord

from AntiSpam.User import User
from AntiSpam.Exceptions import ObjectMismatch, DuplicateObject

"""
This is used to maintain a collection of User's in a relevant guild
"""


class Guild:
    """Represents a guild that maintains a collection of User's

    """

    __slots__ = [
        "_id",
        "_bot",
        "_users",
        "options",
        "logger",
        "has_custom_options",
    ]

    def __init__(self, bot, id, options, *, custom_options=False):
        """

        Parameters
        ----------
        bot: commands.Bot
            The global bot instance
        id : int
            This guilds id
        options : dict
            The options for this guild
        custom_options : bool
            Whether this guild has custom options or not
        """
        self.id = int(id)
        self._bot = bot
        self._users = []
        self.options = deepcopy(options)

        self.has_custom_options = custom_options

    def __repr__(self):
        return (
            f"'{self.__class__.__name__} object. Guild id: {self.id}, "
            f"Len Stored Users {len(self._users)}'"
        )

    def __str__(self):
        return f"{self.__class__.__name__} object for {self.id}."

    def __eq__(self, other):
        """
        This is called with a 'obj1 == obj2' comparison object is made

        Checks against stored id's to figure out if they are
        representing the same User or not

        Parameters
        ----------
        other : Guild
            The object to compare against

        Returns
        -------
        bool
            `True` or `False` depending on whether they are the same or not

        Raises
        ======
        ValueError
            When the comparison object is not of ignore_type `Message`
        """
        if not isinstance(other, Guild):
            raise ValueError("Expected two Guild objects to compare")

        if self.id == other.id:
            return True
        return False

    def __hash__(self):
        """
        Given we create a __eq__ dunder method, we also needed
        to create one for __hash__ lol

        Returns
        -------
        int
            The hash of all id's
        """
        return hash(self.id)

    async def propagate(self, message: discord.Message):
        """
        This method handles a message object and then adds it to
        the relevant member

        Parameters
        ==========
        message : discord.Message
            The message that needs to be propagated out
        
        Returns
        =======
        dict
            A dictionary of useful information about the user in question
        """
        if not isinstance(message, discord.Message) and not isinstance(
            message, MagicMock
        ):
            raise ValueError("Expected message of ignore_type: discord.Message")

        user = User(self._bot, message.author.id, message.guild.id, self.options,)
        try:
            user = next(iter(u for u in self._users if u == user))
        except StopIteration:
            self.users = user
            logging.info(f"Created User: {user.id}")

        return await user.propagate(message)

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        if not isinstance(value, int):
            raise ValueError("Expected integer")
        self._id = value

    @property
    def users(self):
        return self._users

    @users.setter
    def users(self, value):
        """
        Raises
        ======
        DuplicateObject
            It won't maintain two message objects with the same
            id's, and it will complain about it haha
        ObjectMismatch
            Raised if `value` wasn't made by this person, so they
            shouldn't be the ones maintaining the reference
        """
        if not isinstance(value, User):
            raise ValueError("Expected User object")

        if self.id != value.guild_id:
            raise ObjectMismatch

        for user in self._users:
            if user == value:
                raise DuplicateObject

        self._users.append(value)
