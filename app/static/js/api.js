import axios from "axios";


function emailCheck(email) {
    return axios.get("/" + email)
}

export default {
    emailCheck,
}