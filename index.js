import express from 'express';
import mongoose from 'mongoose';
import multer from 'multer';

import { registerValidation, loginValidation, postCreateValidation, handleValitationErrors } from './validations.js';
import { checkAuth } from './utils/index.js';

import { UserController, PostController } from './controllers/index.js'
mongoose
	.connect('mongodb+srv://admin:admin1@cluster0.vvtf7tv.mongodb.net/blog?appName=Cluster0')
	.then(() => console.log('DB ok'))
	.catch((err) => console.log('DB error', err));

const app = express();

const storage = multer.diskStorage({
	destination: (_, __, cb) => {
		cb(null, 'uploads');
	},
	filename: (_, file, cb) => {
		cb(null, file.originalname);
	},
});

const upload = multer({ storage });

//Нужно для правильного чтения json формата в коде
app.use(express.json());
app.use('/uploads', express.static('uploads'));

app.post('/upload', checkAuth, upload.single('image'), (req, res) => {
	res.json({
		url: `/uploads/${req.file.originalname}`,
	});


});

app.post('/auth/register', registerValidation, handleValitationErrors, UserController.register);
app.post('/auth/login', loginValidation, handleValitationErrors, UserController.login);
app.get('/auth/me', checkAuth, UserController.getMe);

app.get('/posts', PostController.getAll);
app.get('/posts/:id', PostController.getOne);
app.post('/posts', checkAuth, postCreateValidation, handleValitationErrors, PostController.create);
app.delete('/posts/:id', checkAuth, PostController.remove);
app.patch('/posts/:id', checkAuth, postCreateValidation, handleValitationErrors, PostController.update);
const PORT = process.env.PORT || 3000;
app.listen(PORT, (err) => {
	if (err) {
		return console.log(err);
	}
	console.log('ServerOk:');
	console.log(PORT);
});
