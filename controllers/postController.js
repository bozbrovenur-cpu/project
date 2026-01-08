import PostModel from '../models/Post.js'

export const update = async (req, res) => {
	try {
		const postId = req.params.id;

		const doc = await PostModel.findOneAndUpdate({
			_id: postId,
		}, {
			title: req.body.title,
			text: req.body.text,
			tags: req.body.tags,
			imageUrl: req.body.imageUrl,
			user: req.body.userId,
		});

		if (!doc) {
			return res.status(404).json({
				message: 'Пост для обновления не найден',
			});
		}

		res.json({
			success: true,
		});
	} catch (err) {
		console.log(err);
		res.status(500).json({
			message: 'Не удалось обновить пост',
		});
	}


}

export const remove = async (req, res) => {
	try {
		const postId = req.params.id;

		const doc = await PostModel.findOneAndDelete({
			_id: postId,
		});

		if (!doc) {
			return res.status(404).json({
				message: 'Невозможно удалить статью',
			});
		}

		res.json({
			success: true,

		});
	} catch (err) {
		console.log(err);
		res.status(500).json({
			message: 'Не удалось удалить статью',
		});
	}

}
export const getOne = async (req, res) => {
	try {
		const postId = req.params.id;

		const doc = await PostModel.findOneAndUpdate({
			_id: postId,
		}, {
			$inc: { viewsCount: 1 },
		}, {
			new: true,
		});
		if (!doc) {
			return res.status(404).json({
				message: 'Статья по айди не не найдена',
			});
		}
		res.json(doc);
	} catch (err) {
		console.log(err);
		res.status(500).json({
			message: 'Ошибка сервера',

		});
	}

}

export const getAll = async (req, res) => {
	try {
		const posts = await PostModel.find().populate('user').exec();

		res.json(posts);
	} catch (err) {
		console.log(err);
		res.status(500).json({
			message: 'Не удалось найти посты',
		});

	}

}
export const create = async (req, res) => {
	try {
		const doc = PostModel({
			title: req.body.title,
			text: req.body.text,
			imageUrl: req.body.imageUrl,
			tags: req.body.tags,
			user: req.userId,
		});

		const post = await doc.save();

		res.json(post);
	} catch (err) {
		console.log(err);
		res.status(500).json({
			message: 'Не получилось создать статью',
		});
	}

}