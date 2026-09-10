from aiogram import Router, types
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import db.insert as insert
import db.select as select
import db.update as update
import db.delete as delete
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import F


class AddTask(StatesGroup):
    waiting_for_text = State()
    waiting_for_deadline = State()





router = Router()

@router.message(CommandStart())
async def start_cmd(message: types.Message):
    if select.does_the_string_exist(message.from_user.id):
        await message.answer('Вы уже зарегистрированы')
    else:
        if insert.registration(message.from_user.id):
            await message.answer('Привет, регистрация завершена')
        else:
            await message.answer('Произошла ошибка')


@router.message(Command('add'))
async def add(message: types.Message, state: FSMContext):
    await state.set_state(AddTask.waiting_for_text)
    await message.answer('Отправьте имя задачи')

@router.message(AddTask.waiting_for_text)
async def get_task_text(message: types.Message, state: FSMContext):
    await state.update_data(task_text=message.text)
    await state.set_state(AddTask.waiting_for_deadline)
    await message.answer('Теперь отправьте дедлайн (в формате ГГГГ-ММ-ДД), либо напишите "нет"')

@router.message(AddTask.waiting_for_deadline)
async def get_task_deadline(message: types.Message, state: FSMContext):
    await state.update_data(task_deadline=message.text)
    data = await state.get_data()
    task_text = data['task_text']
    task_deadline = data['task_deadline']
    if insert.add_task(task_text, task_deadline, message.from_user.id):
        await state.clear()
        await message.answer('Ваша задача успешно сохранена')
    else:
        await message.answer('Произошла ошибка')


@router.message(Command('task_list'))
async def task_list_cmd(message: types.Message):
    tasks = select.task_list(message.from_user.id)
    if tasks:
        for task in tasks:
            task_id = task[0]
            if task[3] == 1:
                await message.answer(f'ЗАДАЧА:  {task[1]}, ДЕДЛАЙН:  {task[2]}, СТАТУС:  ВЫПОЛНЕНО', reply_markup=get_task_keyboard(task_id))
            else:
                await message.answer(f'ЗАДАЧА:  {task[1]}, ДЕДЛАЙН:  {task[2]}, СТАТУС:  НЕ ВЫПОЛНЕНО', reply_markup=get_task_keyboard(task_id))
    else:
        await message.answer('У вас пока нет задач')

def get_task_keyboard(task_id):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Выполнено", callback_data=f"done_{task_id}"),
            InlineKeyboardButton(text="🗑 Удалить", callback_data=f"delete_{task_id}")
        ]
    ])
    return keyboard




@router.callback_query(F.data.startswith("done_"))
async def handle_done(callback: types.CallbackQuery):
    split_data = callback.data.split('_')
    if update.update_status(split_data[1]):
        await callback.answer("Действие обработано: ЗАДАЧА ВЫПОЛНЕНА")
    else:
        await callback.answer("ОШИБКА: Действие обработано не корректно")
    

@router.callback_query(F.data.startswith("delete_"))
async def handle_delete(callback: types.CallbackQuery):
    split_data = callback.data.split('_')
    if delete.delete(split_data[1]):
        await callback.answer("Действие обработано: ЗАДАЧА удалена")
    else:
        await callback.answer("ОШИБКА: Действие обработано не корректно")


@router.message(Command('help'))
async def help(message:types.Message):
    await message.answer(f'Что умеет бот:\n/start -> Регистрация пользователя\n/add -> Добавляет задачу и дедлайн пользователя\n/task_list -> Выдает список задач пользователя с кнопками на изменение статуса и удаление задачи')