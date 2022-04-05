export default class ServerApi {
    static skills = `/api/skills`;

    static companies = `/api/companies`;

    static pbhCompanies = `/api/pbh_companies`;

    static vacancyList = `/api/vacancy_list`;

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

    static async getCompanies() {
        const response = await fetch(
            `${ServerApi.companies}`,
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

    static async getPbhCompanies() {
        const response = await fetch(
            `${ServerApi.pbhCompanies}`,
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
