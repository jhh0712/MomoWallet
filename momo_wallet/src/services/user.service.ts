import axios from 'axios';
import App from '../App';
import authHeader from './auth-header';
import { app } from 'electron';

const API_URL = 'http://localhost:8080/api/';

class UserService {
    getPublicContent() {
        let app_version = 1234;
        return axios.post(API_URL + 'home/get-version/post/', {
            app_version
        });
    }

    getUserBoard() {
        return axios.get(API_URL + 'user', { headers: authHeader() });
    }

    getModeratorBoard() {
        return axios.get(API_URL + 'mod', { headers: authHeader() });
    }

    getAdminBoard() {
        return axios.get(API_URL + 'admin', { headers: authHeader() });
    }
}

export default new UserService();