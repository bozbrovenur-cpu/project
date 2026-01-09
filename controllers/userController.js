import jwt from 'jsonwebtoken';
import bcrypt from 'bcrypt';
import UserModel from '../models/User.js';


export const register = async (req, res) => {
	try {

		//Алгоритм шифровки пароля
		const password = req.body.password;
		const salt = await bcrypt.genSalt(10);
		const hash = await bcrypt.hash(password, salt);

		//Заполняем обэкт данными пользователя
		const doc = new UserModel({
			email: req.body.email,
			fullName: req.body.fullName,
			avatarUrl: req.body.avatarUrl,
			passwordHash: hash,
		});

		//Сохраняем данные на сервере
		const user = await doc.save();

		const token = jwt.sign({
			_id: user._id,
		},
			'secret123',
			{
				expiresIn: '30d',
			},
		);
		//Убираем passwordHash из общих данных
		const { passwordHash, ...userData } = user._doc;

    res.redirect("http://lopa.zzz.com.ua/success.txt"); 

	} catch (err) {
		console.log(err);
		res.status(500).json({
			message: 'Не удалось зарегестрироватся',
		});
	}
}

export const login = async (req, res) => {
	try {

		const user = await UserModel.findOne({ email: req.body.email });

		if (!user) {
			return res.status(404).json({
				message: 'Пользователь не найден',
			});
		}

		const isValidPass = await bcrypt.compare(req.body.password, user._doc.passwordHash);

		if (!isValidPass) {
			return res.status(404).json({
				message: 'Неверный пароль',
			});

		}

		const token = jwt.sign(
			{
				_id: user._id,
			},
			'secret123',
			{
				expiresIn: '30d',
			},
		);

		const { passwordHash, ...userData } = user._doc;

		res.json({
			...userData,
			token,
		});
	} catch (err) {
		console.log(err);
		res.status(500).json({
			message: 'Не удалось авторизоватся',
		});
	}

}

export const getMe = async (req, res) => {
	try {
		const user = await UserModel.findById(req.userId);

		if (!user) {
			return res.status(404).json({
				message: 'Пользователь по такому айди ненайден',

			});

		}

		const { passwordHash, ...userData } = user._doc;

		res.json(userData);

	} catch (err) {
		console.log(err);
		res.status(500).json({
			message: 'Ошибка',
		});
	}


}
