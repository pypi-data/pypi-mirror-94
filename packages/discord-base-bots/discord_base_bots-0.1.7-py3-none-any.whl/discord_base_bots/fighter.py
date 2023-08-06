import random
import itertools
import json

from discord_base_bots.base import BaseBot, run_bot


class Fighter(BaseBot):

    bot_name = None
    hot_word = None

    def __init__(self, *args, health=50, endurance=30, **kwargs):
        """

        Args:
            health (int): fighter total health.
            endurance (int): number of seconds a fighter can last
        """
        super().__init__(*args, **kwargs)

        self.health = health
        self.endurance = endurance
        self.current_health = health
        self.current_endurance = endurance
        self.fighting = False
        self.opponent = ""
        self.advantage = None
        self.defending = False
        self.__victory = False

        commands = {
            "init_fight": self.init_fight,
            "fight": self.fight,
            "wins": self.__on_victory
        }
        self.update_commands(commands)

    async def init_fight(self, command_content, message):
        # self.__timer = asyncio.create_task(self.fight_timer())
        self.fighting = True
        fight_data = json.loads(command_content)
        self.opponent = fight_data['opponent']
        self.advantage = fight_data['advantage'] == self.hot_word
        print("---initing generator")
        self.fight_loop = self.execute_fight()
        print("---print sending primer")
        await self.fight_loop.asend(None)  # Prime
        print(f'checking advantage: {self.advantage}')
        if self.advantage:
            await self.fight(command_content, message)

    async def fight(self, command_content, message):
        if self.fighting and self.fight_loop:
            print("sending to fight loop")
            await self.fight_loop.asend((command_content, message))

    async def execute_fight(self):
        offense_flow = [self.__action, self.__read_reaction]
        defense_flow = [self.__read_action]
        if self.advantage:
            temp_action_list = offense_flow + defense_flow
            action_list = itertools.cycle(temp_action_list)
        else:
            action_list = itertools.cycle(defense_flow + offense_flow)
        data, message = yield

        while self.current_health >= 0 and self.current_endurance >= 0 and not self.__victory:
            print("top of loop")
            activity = next(action_list)
            print(activity)
            await activity(data, message)
            print("activity complete")
            data, message = yield
        if self.current_health <= 0:
            await self.__on_loss(data, message)
        if self.current_endurance <= 0:
            await self.__on_timeout(data, message)
        self.__reset_fighter()

    async def __send_fight_data(self, data, message):
        string = f"{self.opponent} fight {data}"
        await message.channel.send(string)

    async def __send_ref_data(self, data, message):
        await message.channel.send(f"refbot {data}")

    async def __action(self, data, message):
        """Bot takes an action.

        This action can be to attack or defend.
        Performing an action costs endurance.
        """
        print("Running action")
        data = self.action()
        if data == "defend":
            self.defending = True
        else:
            self.defending = False
        self.current_endurance -= 1
        await self.__send_fight_data(data, message)

    async def __read_action(self, action, message):
        """Process what the opponent did and react to it.

        Perform a reaction and send it back to the opponent.
        """
        """React to what your opponent did for their round action."""
        print("Running read action")
        if f"attack" in action:
            if self.defending or random.randint(1, 100) > 95:
                self.current_health -= 3
                reaction = f"_reacts_: {self.hot_word} blocks the attack"
            else:
                self.current_health -= 10
                reaction = f"_reacts_: {self.hot_word} is hit by the attack"
        else:
            reaction = ""
        response = self.process_opponent_action(action)
        if response:
            await message.channel.send(response)
        await self.__send_fight_data(reaction, message)

    async def __read_reaction(self, reaction, message):
        """Process how the opponent reacted to your action"""
        print("Running read reaction")
        confirmation = self.read_reaction(reaction)
        if confirmation and isinstance(confirmation, str):
            confirmation = "_responds_: "+confirmation.strip()
            await message.channel.send(confirmation)
        await message.channel.send(f"Health: {self.current_health}, Endurance: {self.current_endurance}")
        await self.__send_ref_data(f"bow {self.opponent}", message)

    def __read_confirmation(self, confirmation, message):
        if confirmation:
            return True
        else:
            return False

    async def __process_end_fight_statements(self, data, message):
        statements = []
        if isinstance(data, str):
            statements.append(data)
        elif isinstance(data, list):
            statements = data
        for statement in statements:
            await message.channel.send(statement)

    async def __on_victory(self, data, message):
        self.__victory = True
        user_messages = self.on_victory(data, message)
        await self.__process_end_fight_statements(user_messages, message)
        self.__reset_fighter()

    async def __on_loss(self, data, message):
        user_messages = self.on_loss(data, message)
        await self.__process_end_fight_statements(user_messages, message)
        await self.__send_ref_data(f"yield health {self.opponent}", message)

    async def __on_timeout(self, data, message):
        user_messages = self.on_timeout(self, data, message)
        await self.__process_end_fight_statements(user_messages, message)
        await self.__send_ref_data(f"yield exhausted {self.opponent}", message)

    def __reset_fighter(self):
        # TODO these should really all be __private
        self.advantage = None
        self.timer = None
        self.fighting = False
        self.defending = False
        self.current_health = self.health
        self.current_endurance = self.endurance
        self.__victory = False

    # async def fight_timer(self):
    #     await asyncio.sleep(self.endurance)
    #     try:
    #         self.fight_loop._cancel()
    #         self.fight_loop = None
    #         self.__reset_fighter()
    #     except Exception as e:
    #         pass

    #############################
    #
    # Your round actions
    #
    #############################
    def action(self, *args):
        """What do you want to do this round?"""
        return random.choice(["attack", "defend"])

    def read_reaction(self, reaction):
        """Read how your opponent reacted to your round action."""
        if f"{self.opponent} blocks" in reaction:
            return f"{self.hot_word} staggers back"

    #############################
    #
    # Opponent round actions
    #
    #############################
    def process_opponent_action(self, action):
        """View the action your opponent took.

        Args:
            action (str): The action your opponent took this round.

        Returns:
            Optional[str]: A text response to the action.
        """
        if action.endswith("defend"):
                return "_searches your defence_"
        elif action.endswith("attack"):
                return "_attempts to counter_"

    #############################
    #
    # End conditions
    #
    #############################
    def on_victory(self, data, message):
        messages = [
            "Victory is mine",
            f"void sacrifice {self.opponent}"]
        return messages

    def on_loss(self, data, message):
        return "I have failed"

    def on_timeout(self, data, message):
        return "I can't go on"


if __name__ == "__main__":
    from pathlib import Path

    class FightBot(Fighter):
        bot_name = "FightBot"
        hot_word = "fightbot"

    run_bot(FightBot, Path(".env").resolve())
