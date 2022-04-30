from aiogram.dispatcher.filters.state import StatesGroup, State


class ReScrum(StatesGroup):
    Q1 = State()
    Q2 = State()
    Q3 = State()
    Q4 = State()


class ReTasks(StatesGroup):
    T1 = State()
    T2 = State()
    T3 = State()
    T4 = State()


class IDAdmin(StatesGroup):
    I1 = State()
    I2 = State()


class AdminTasks(StatesGroup):
    AT1 = State()
    AT2 = State()
    AT3 = State()
    AT4 = State()


class Sprint(StatesGroup):
    S1 = State()
    S2 = State()
    S3 = State()


class Retro(StatesGroup):
    R1 = State()
    R2 = State()
    R3 = State()
    R4 = State()


class Good(StatesGroup):
    G1 = State()
    G2 = State()


class MoodRETRO(StatesGroup):
    M1 = State()
    M2 = State()


class Bad(StatesGroup):
    B1 = State()
    B2 = State()


class getRetro(StatesGroup):
    gR1 = State()
    gR2 = State()


class Task_done(StatesGroup):
    Td = State()
