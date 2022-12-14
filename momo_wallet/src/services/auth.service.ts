import axios from "axios";

class AuthService {
    login(username: string, password: string) {
        return axios.post("/api/auth/signin/post/", {
            username,
            password
        })
        .then(response => {
            if (response.data.access) {
                localStorage.setItem("user", JSON.stringify(response.data));
            }
            return response.data;
        });
    }
    
    logout() {
        localStorage.removeItem("user");
    }
    
    register(username: string, email: string, password: string) {
        return axios.post("/api/auth/signup/post/", {
            username,
            email,
            password
        });
    }

    getCurrentUser() {
        const userStr = localStorage.getItem("user");
        if (userStr) {
            return JSON.parse(userStr);
        }
        return null;
    }
}

export default new AuthService();