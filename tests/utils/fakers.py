from src.game.game import Stage, Game


def get_dummy_stage() -> Stage:
    stage = Stage("fake_id", 1)
    stage.data['words'] = "test1,test2,test3,test4"
    return stage


def get_dummy_game() -> Game:
    return Game("fake_username")
