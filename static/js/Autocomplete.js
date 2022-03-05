import ServerApi from './ServerApi.js';

export class Autocomplete {
    static names;

    static includedSkills = [];

    static excludedSkills = [];

    setSkills(names) {
        Autocomplete.names = [...names];
    }

    static containerClearAndHide() {
        const autocompleteContainer = document.querySelector('.autocomplete-list');
        const searchInput = document.querySelector('.form-specs__search');
        const overlay = document.querySelector('.overlay');

        autocompleteContainer.classList.remove('autocomplete-list_visible');
        searchInput.classList.remove('search_active');
        overlay.classList.remove('overlay_visible');
        autocompleteContainer.removeEventListener('click', Autocomplete.changeFinalList);
    }

    static renderNames(arrayOfNames) {
        const autocompleteContainer = document.querySelector('.autocomplete-list');
        const searchInput = document.querySelector('.form-specs__search');
        autocompleteContainer.classList.add('autocomplete-list_visible');
        searchInput.classList.add('search_active');

        let liElements = '';
        for (let i = 0; i < arrayOfNames.length; i++) {
            liElements += `
                <li class="autocomplete-list__item" data-name=${arrayOfNames[i].id}>
                    <div class="autocomplete-text-wrapper">
                        <p class="autocomplete-text" id="${arrayOfNames[i].id}">${arrayOfNames[i].name}</p> 
                        <span>(${arrayOfNames[i].num})</span>
                    </div>
                    <div class="autocomplete-buttons-wrapper">
                        <button class="button autocomplete-button" id="autocomplete-add" type="button">
                          <svg class="autocomplete-button__icon" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"  fill="#ffffff"><path d="M24 10h-10v-10h-4v10h-10v4h10v10h4v-10h10z"/></svg>
                        </button>
                        <button class="button autocomplete-button" id="autocomplete-remove" type="button">
                          <svg class="autocomplete-button__icon" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="#ffffff"><path d="M0 10h24v4h-24z"/></svg>
                        </button>
                    </div>
               </li>`;
        }
        autocompleteContainer.innerHTML = liElements;
        autocompleteContainer.addEventListener('click', Autocomplete.changeFinalList);
    }

    filterForNames(event) {
        const searchValue = event.target.value.toLowerCase();
        const overlay = document.querySelector('.overlay');

        if (searchValue === '') {
            Autocomplete.containerClearAndHide();
        } else {
            const filteredNames = Autocomplete.names.filter((v, i) => {
                const skill = v.name;
                if (skill) {
                    return (skill.toLowerCase().includes(searchValue));
                }
            });

            if (filteredNames.length === 0) {
                Autocomplete.containerClearAndHide();
            } else {
                event.target.focus();
                Autocomplete.renderNames(filteredNames);
                overlay.classList.add('overlay_visible');
            }
        }
    }

    static changeFinalList(event) {
        const searchInput = document.querySelector('.form-specs__search');
        searchInput.focus();


        if (event.target.closest('.autocomplete-button')) {
            const selectedSkillsElement = document.querySelector('.form-specs__selected-skills');

            const skillId = Number(event
                .target
                .closest('.autocomplete-list__item')
                .getAttribute('data-name'));

            const skillObject = Autocomplete.names.find((skill) => {
                return skill.id === skillId;
            });

            if (event.target.closest('#autocomplete-add')) {
                if (!Autocomplete.isSkillContained(skillId, true)
                    && !Autocomplete.isSkillContained(skillId, false)) {
                    Autocomplete.includedSkills.push(skillObject);
                } else if (!Autocomplete.isSkillContained(skillId, true)
                    && Autocomplete.isSkillContained(skillId, false)) {
                    Autocomplete.includedSkills.push(skillObject);

                    const skillIndex = Autocomplete.excludedSkills.findIndex(skill => skill.id === skillId);
                    Autocomplete.excludedSkills.splice(skillIndex, 1);
                    Autocomplete.deleteSkillWithIndex(skillId, false);
                }
            } else if (event.target.closest('#autocomplete-remove')) {
                if (!Autocomplete.isSkillContained(skillId, false)
                    && !Autocomplete.isSkillContained(skillId, true)) {
                    Autocomplete.excludedSkills.push(skillObject);
                } else if (!Autocomplete.isSkillContained(skillId, false)
                    && Autocomplete.isSkillContained(skillId, true)) {
                    Autocomplete.excludedSkills.push(skillObject);

                    const skillIndex = Autocomplete.includedSkills.findIndex(skill => skill.id === skillId);
                    Autocomplete.includedSkills.splice(skillIndex, 1);
                    Autocomplete.deleteSkillWithIndex(skillId, true);
                }
            }

            let skills = '';

            Autocomplete.includedSkills.forEach((skill) => {
                skills += `
                    <button 
                      class="button selected-skill selected-skill_included" 
                      data-name=${skill.id}
                      type="button"
                    >${skill.name}</button>
                `
            });

            Autocomplete.excludedSkills.forEach((skill) => {
                skills += `
                    <button 
                      class="button selected-skill selected-skill_excluded" 
                      data-name=${skill.id}
                      type="button"
                    >${skill.name}</button>
                `
            });

            selectedSkillsElement.innerHTML = skills;
        }
    }

    static isSkillContained(skillId, included) {
        if (included) {
            return Autocomplete.includedSkills.some(skill => skill.id === skillId);
        } else {
            return Autocomplete.excludedSkills.some(skill => skill.id === skillId);
        }

    }

    closeContainer(event) {
        const searchInput = document.querySelector('.form-specs__search');
        event.target.classList.remove('overlay_visible');

        searchInput.blur();
        Autocomplete.containerClearAndHide();

    }

    deleteSkillWithEvent(event) {
        if (event.target.classList.contains('selected-skill')) {
            if (event.target.classList.contains('selected-skill_included')) {
                const skillIndex = Autocomplete.includedSkills.findIndex(skill => skill.id === Number(event.target.getAttribute('data-name')));
                if (skillIndex !== -1) {
                    Autocomplete.includedSkills.splice(skillIndex, 1);
                    event.target.remove();
                }
            } else if (event.target.classList.contains('selected-skill_excluded')) {
                const skillIndex = Autocomplete.excludedSkills.findIndex(skill => skill.id === Number(event.target.getAttribute('data-name')));
                if (skillIndex !== -1) {
                    Autocomplete.excludedSkills.splice(skillIndex, 1);
                    event.target.remove();
                }
            }
        }
    }

    static deleteSkillWithIndex(skillId, included) {
        if (included) {
            const skillElement = document.querySelector(`.selected-skill_included[data-name="${skillId}"]`);
            skillElement.remove();
        } else {
            const skillElement = document.querySelector(`.selected-skill_excluded[data-name="${skillId}"]`);
            skillElement.remove();
        }
    }

    async submitForm(event) {
        event.preventDefault();

        let skillOnData = [];
        let skillOffData = [];

        Autocomplete.includedSkills.forEach((skill) => {
            skillOnData.push(skill.id);
        });

        Autocomplete.excludedSkills.forEach((skill) => {
            skillOffData.push(skill.id);
        });

        const formData = [];

        skillOnData.forEach((id) => {
            formData.push(['skill_on_id', id]);
        })

        skillOffData.forEach((id) => {
            formData.push(['skill_off_id', id]);
        })

        const params = Autocomplete.encodeQueryDataArray(formData);
        document.location.href = `${ServerApi.vacancyList}?${params}`;
    }

    static encodeQueryDataArray(data) {
        let req = [];
        data.forEach((el) => {
            req.push(encodeURIComponent(el[0]) + '=' + encodeURIComponent(el[1]));
        })
        return req.join('&');
    }

    clearAll() {
        const selectedSkillElement = document.querySelector('.form-specs__selected-skills');
        selectedSkillElement.innerHTML = '';
        Autocomplete.includedSkills = [];
        Autocomplete.excludedSkills = [];
    }

    startAutocomplete() {
        const searchInput = document.querySelector('.form-specs__search');
        const overlay = document.querySelector('.overlay');
        const selectedSkillElement = document.querySelector('.form-specs__selected-skills');
        const searchForm = document.getElementById('searchForm');

        searchInput.addEventListener('input', this.filterForNames);
        searchInput.addEventListener('focus', this.filterForNames);
        overlay.addEventListener('click', this.closeContainer);
        selectedSkillElement.addEventListener('click', this.deleteSkillWithEvent);
        searchForm.addEventListener('submit', this.submitForm);
        searchForm.addEventListener('reset', this.clearAll);
    }
}
