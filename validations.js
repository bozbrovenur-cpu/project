import { body } from 'express-validator';
import { validationResult } from 'express-validator';

export const loginValidation = [
	body('email', 'Неверный формат почты').isEmail(),
	body('password', 'Минимальная длина пароля 5 символов').isLength({ min: 5 }),

];

export const registerValidation = [
	body('email', 'Неверный формат почты').isEmail(),
	body('password', 'Минимальная длина пароля 5 символов').isLength({ min: 5 }),
	body('fullName', 'Минимальная длина имени 3 символа').isLength({ min: 3 }),
	body('avatarUrl', 'Неверная сыллка на аватарку').optional().isURL(),
];

export const postCreateValidation = [
	body('title', 'Нужно ввести заголовок').isLength({ min: 4 }).isString(),
	body('text', 'Нужно ввести текст').isLength({ min: 10 }).isString(),
	body('tags', 'Нужно ввести тег').optional().isArray(),
	body('imageUrl', 'Нужно ввесты сыллку на изображение').optional().isString(),
];

export const handleValitationErrors = (req, res, next) => {
	//Проверяем корректнсть полученных данных от пользователя
	const errors = validationResult(req);
	if (!errors.isEmpty()) {
		return res.status(400).json(errors.array());
	}

	next();
}