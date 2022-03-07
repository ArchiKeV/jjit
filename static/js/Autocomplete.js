import ServerApi from './ServerApi.js';

export class Autocomplete {
    constructor() {
        this.changeFinalList = this.changeFinalList.bind(this);
        this.filterForNames = this.filterForNames.bind(this);
        this.closeContainer = this.closeContainer.bind(this);
        this.deleteSkillWithEvent = this.deleteSkillWithEvent.bind(this);
        this.submitForm = this.submitForm.bind(this);
        this.clearAll = this.clearAll.bind(this);
    }

    names;

    included = [];

    excluded = [];

    setSkills(names) {
        this.names = [...names];
    }

    containerClearAndHide() {
        const autocompleteContainer = document.querySelector('.autocomplete-list');
        const searchInput = document.querySelector('.form-specs__search');
        const overlay = document.querySelector('.overlay');

        autocompleteContainer.classList.remove('autocomplete-list_visible');
        searchInput.classList.remove('search_active');
        overlay.classList.remove('overlay_visible');
        autocompleteContainer.removeEventListener('click', this.changeFinalList);
    }

    renderNames(arrayOfNames) {
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
        autocompleteContainer.addEventListener('click', this.changeFinalList);
    }

    filterForNames(event) {
        const searchValue = event.target.value.toLowerCase();
        const overlay = document.querySelector('.overlay');

        if (searchValue === '') {
            this.containerClearAndHide();
        } else {
            const filteredNames = this.names.filter((v) => {
                const skill = v.name;
                if (skill) {
                    return (skill.toLowerCase().includes(searchValue));
                }
            });

            if (filteredNames.length === 0) {
                this.containerClearAndHide();
            } else {
                event.target.focus();
                this.renderNames(filteredNames);
                overlay.classList.add('overlay_visible');
            }
        }
    }

    changeFinalList(event) {
        const searchInput = document.querySelector('.form-specs__search');
        searchInput.focus();


        if (event.target.closest('.autocomplete-button')) {
            const selectedSkillsElement = document.querySelector('.form-specs__selected-skills');
            const hiddenInputsElement = document.querySelector('.form-specs__hidden-inputs');

            const skillId = Number(event
                .target
                .closest('.autocomplete-list__item')
                .getAttribute('data-name'));

            const skillObject = this.names.find((skill) => {
                return skill.id === skillId;
            });

            if (event.target.closest('#autocomplete-add')) {
                if (!this.isSkillContained(skillId, true)
                    && !this.isSkillContained(skillId, false)) {
                    this.included.push(skillObject);
                } else if (!this.isSkillContained(skillId, true)
                    && this.isSkillContained(skillId, false)) {
                    this.included.push(skillObject);

                    const skillIndex = this.excluded.findIndex(skill => skill.id === skillId);
                    this.excluded.splice(skillIndex, 1);
                    this.deleteSkillWithIndex(skillId, false);
                    this.deleteSkillInput(skillId, false);
                }
            } else if (event.target.closest('#autocomplete-remove')) {
                if (!this.isSkillContained(skillId, false)
                    && !this.isSkillContained(skillId, true)) {
                    this.excluded.push(skillObject);
                } else if (!this.isSkillContained(skillId, false)
                    && this.isSkillContained(skillId, true)) {
                    this.excluded.push(skillObject);

                    const skillIndex = this.included.findIndex(skill => skill.id === skillId);
                    this.included.splice(skillIndex, 1);
                    this.deleteSkillWithIndex(skillId, true);
                    this.deleteSkillInput(skillId, true);
                }
            }

            let skills = '';
            let inputs = '';

            this.included.forEach((skill) => {
                skills += `
                    <button 
                      class="button selected-skill selected-skill_included" 
                      data-name=${skill.id}
                      type="button"
                    >${skill.name}</button>
                `
            });

            this.excluded.forEach((skill) => {
                skills += `
                    <button 
                      class="button selected-skill selected-skill_excluded" 
                      data-name=${skill.id}
                      type="button"
                    >${skill.name}</button>
                `
            });

            this.included.forEach((skill) => {
                inputs += `
                    <input 
                      class="hidden-input_included"
                      name="skill_on_id" 
                      data-name=${skill.id}
                      type="checkbox"
                      value=${skill.id}
                      checked
                    />
                `
            });

            this.excluded.forEach((skill) => {
                inputs += `
                    <input 
                      class="hidden-input_excluded" 
                      name="skill_off_id"
                      data-name=${skill.id}
                      type="checkbox"
                      value=${skill.id}
                      checked
                    />
                `
            });

            selectedSkillsElement.innerHTML = skills;
            hiddenInputsElement.innerHTML = inputs;
        }
    }

    isSkillContained(skillId, included) {
        if (included) {
            return this.included.some(skill => skill.id === skillId);
        } else {
            return this.excluded.some(skill => skill.id === skillId);
        }

    }

    closeContainer(event) {
        const searchInput = document.querySelector('.form-specs__search');
        event.target.classList.remove('overlay_visible');

        searchInput.blur();
        this.containerClearAndHide();

    }

    deleteSkillWithEvent(event) {
        if (event.target.classList.contains('selected-skill')) {
            if (event.target.classList.contains('selected-skill_included')) {
                const skillIndex = this.included.findIndex(skill => skill.id === Number(event.target.getAttribute('data-name')));
                if (skillIndex !== -1) {
                    this.included.splice(skillIndex, 1);
                    event.target.remove();
                    this.deleteSkillInput(skillIndex, true);
                }
            } else if (event.target.classList.contains('selected-skill_excluded')) {
                const skillIndex = this.excluded.findIndex(skill => skill.id === Number(event.target.getAttribute('data-name')));
                if (skillIndex !== -1) {
                    this.excluded.splice(skillIndex, 1);
                    event.target.remove();
                    this.deleteSkillInput(skillIndex, false);
                }
            }
        }
    }

    deleteSkillWithIndex(skillId, included) {
        if (included) {
            const skillElement = document.querySelector(`.selected-skill_included[data-name="${skillId}"]`);
            skillElement.remove();
        } else {
            const skillElement = document.querySelector(`.selected-skill_excluded[data-name="${skillId}"]`);
            skillElement.remove();
        }
    }

    deleteSkillInput(skillId, included) {
        if (included) {
            const skillElement = document.querySelector(`.hidden-input_included[data-name="${skillId}"]`);
            skillElement.remove();
        } else {
            const skillElement = document.querySelector(`.hidden-input_excluded[data-name="${skillId}"]`);
            skillElement.remove();
        }
    }

    async submitForm(event) {
        event.preventDefault();

        let skillOnData = [];
        let skillOffData = [];

        this.included.forEach((skill) => {
            skillOnData.push(skill.id);
        });

        this.excluded.forEach((skill) => {
            skillOffData.push(skill.id);
        });

        const formData = [];

        skillOnData.forEach((id) => {
            formData.push(['skill_on_id', id]);
        })

        skillOffData.forEach((id) => {
            formData.push(['skill_off_id', id]);
        })

        const params = this.encodeQueryDataArray(formData);
        document.location.href = `${ServerApi.vacancyList}?${params}`;
    }

    encodeQueryDataArray(data) {
        let req = [];
        data.forEach((el) => {
            req.push(encodeURIComponent(el[0]) + '=' + encodeURIComponent(el[1]));
        })
        return req.join('&');
    }

    clearAll() {
        const selectedSkillElement = document.querySelector('.form-specs__selected-skills');
        const hiddenInputsElement = document.querySelector('.form-specs__hidden-inputs');
        selectedSkillElement.innerHTML = '';
        hiddenInputsElement.innerHTML = '';
        this.included = [];
        this.excluded = [];
    }

    startAutocomplete() {
        const searchInput = document.querySelector('.form-specs__search');
        const overlay = document.querySelector('.overlay');
        const selectedSkillElement = document.querySelector('.form-specs__selected-skills');
        const searchForm = document.querySelector('.form-specs');

        searchInput.addEventListener('input', this.filterForNames);
        searchInput.addEventListener('focus', this.filterForNames);
        overlay.addEventListener('click', this.closeContainer);
        selectedSkillElement.addEventListener('click', this.deleteSkillWithEvent);
        searchForm.addEventListener('reset', this.clearAll);
    }
}
