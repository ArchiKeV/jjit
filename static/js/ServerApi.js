export default class ServerApi {
    static baseApiURL = 'http://127.0.0.1:8000/api';

    static baseURL = 'http://127.0.0.1:8000';

    static skills = `${ServerApi.baseApiURL}/skills`;

    static vacancyList = `${ServerApi.baseURL}/vacancy_list`;

    static async getSkills() {
        const response = await fetch(
            `${ServerApi.skills}`,
            {
                method: 'GET',
                headers: {
                    Accept: 'application/json',
                },
            }
        );
        if (!response.ok) {
            console.log(
                `Sorry, but there is ${response.status} error: ${response.statusText}`
            );
            return [];
        }
        return response.json();
    }
}
