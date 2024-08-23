export const fetchUrlInfo = async (username) => {
    const response = await fetch(`http://127.0.0.1:5000/user_info?username=${username}`)
    const data = await response.json();
    return data;
};