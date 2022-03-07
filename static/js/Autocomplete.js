import ServerApi from './ServerApi.js';

export class Autocomplete {
    constructor() {
        this.changeFinalList = this.changeFinalList.bind(this);
        this.filterForNames = this.filterForNames.bind(this);
        this.closeContainer = this.closeContainer.bind(this);
        this.deleteNameWithEvent = this.deleteNameWithEvent.bind(this);
        this.submitForm = this.submitForm.bind(this);
        this.clearAll = this.clearAll.bind(this);
        this.createHTML = this.createHTML.bind(this);
    }

    formName = '';

    excludedFieldName = '';

    includedFieldName = '';

    names;

    included = [];

    excluded = [];

    setNames(names) {
        this.names = [...names];
    }

    setFormName(name) {
        this.formName = name;
    }

    setExFieldName(name) {
        this.excludedFieldName = name;
    }

    setInFieldName(name) {
        this.includedFieldName = name;
    }

    containerClearAndHide() {
        const autocompleteContainer = document.getElementById(`autocompleteList${this.formName}`);
        const searchInput = document.getElementById(`searchInput${this.formName}`);
        const overlay = document.getElementById(`overlay${this.formName}`);

        autocompleteContainer.classList.remove('autocomplete-list_visible');
        searchInput.classList.remove('search_active');
        overlay.classList.remove('overlay_visible');
        autocompleteContainer.removeEventListener('click', this.changeFinalList);
    }

    renderNames(arrayOfNames) {
        const autocompleteContainer = document.getElementById(`autocompleteList${this.formName}`);
        const searchInput = document.getElementById(`searchInput${this.formName}`);
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
        const overlay = document.getElementById(`overlay${this.formName}`);

        if (searchValue === '') {
            this.containerClearAndHide();
        } else {
            const filteredNames = this.names.filter((v) => {
                const name = v.name;
                if (name) {
                    return (name.toLowerCase().includes(searchValue));
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
        const searchInput = document.getElementById(`searchInput${this.formName}`);
        searchInput.focus();

        if (event.target.closest('.autocomplete-button')) {
            const selectedNamesElement = document.getElementById(`selectedNames${this.formName}`);
            const hiddenInputsElement = document.getElementById(`hiddenInputs${this.formName}`);

            const nameId = event
                .target
                .closest('.autocomplete-list__item')
                .getAttribute('data-name');

            const nameObject = this.names.find((name) => {
                return name.id === nameId;
            });

            if (event.target.closest('#autocomplete-add')) {
                if (!this.isNameContained(nameId, true)
                    && !this.isNameContained(nameId, false)) {
                    this.included.push(nameObject);
                } else if (!this.isNameContained(nameId, true)
                    && this.isNameContained(nameId, false)) {
                    this.included.push(nameObject);

                    const skillIndex = this.excluded.findIndex(skill => skill.id === nameId);
                    this.excluded.splice(skillIndex, 1);
                    this.deleteNameWithIndex(nameId, false);
                    this.deleteNameInput(nameId, false);
                }
            } else if (event.target.closest('#autocomplete-remove')) {
                if (!this.isNameContained(nameId, false)
                    && !this.isNameContained(nameId, true)) {
                    this.excluded.push(nameObject);
                } else if (!this.isNameContained(nameId, false)
                    && this.isNameContained(nameId, true)) {
                    this.excluded.push(nameObject);

                    const nameIndex = this.included.findIndex(name => name.id === nameId);
                    this.included.splice(nameIndex, 1);
                    this.deleteNameWithIndex(nameId, true);
                    this.deleteNameInput(nameId, true);
                }
            }

            let names = '';
            let inputs = '';

            this.included.forEach((name) => {
                names += `
                    <button 
                      class="button selected-name selected-name_included" 
                      data-name=${name.id}
                      type="button"
                    >${name.name}</button>
                `
            });

            this.excluded.forEach((name) => {
                names += `
                    <button 
                      class="button selected-name selected-name_excluded" 
                      data-name=${name.id}
                      type="button"
                    >${name.name}</button>
                `
            });

            this.included.forEach((name) => {
                inputs += `
                    <input 
                      class="hidden-input_included"
                      name=${this.includedFieldName} 
                      data-name=${name.id}
                      type="checkbox"
                      value=${name.id}
                      checked
                    />
                `
            });

            this.excluded.forEach((name) => {
                inputs += `
                    <input 
                      class="hidden-input_excluded" 
                      name=${this.excludedFieldName} 
                      data-name=${name.id}
                      type="checkbox"
                      value=${name.id}
                      checked
                    />
                `
            });

            selectedNamesElement.innerHTML = names;
            hiddenInputsElement.innerHTML = inputs;
        }
    }

    isNameContained(nameId, included) {
        if (included) {
            return this.included.some(name => name.id === nameId);
        } else {
            return this.excluded.some(name => name.id === nameId);
        }
    }

    closeContainer(event) {
        const searchInput = document.getElementById(`searchInput${this.formName}`);
        event.target.classList.remove('overlay_visible');

        searchInput.blur();
        this.containerClearAndHide();

    }

    deleteNameWithEvent(event) {
        if (event.target.classList.contains('selected-name')) {
            if (event.target.classList.contains('selected-name_included')) {
                const nameIndex = this.included.findIndex(name => name.id === event.target.getAttribute('data-name'));
                const nameId = event.target.getAttribute('data-name');
                if (nameIndex !== -1) {
                    this.included.splice(nameIndex, 1);
                    event.target.remove();
                    this.deleteNameInput(nameId, true);
                }
            } else if (event.target.classList.contains('selected-name_excluded')) {
                const nameIndex = this.excluded.findIndex(name => name.id === event.target.getAttribute('data-name'));
                const nameId = event.target.getAttribute('data-name');
                if (nameIndex !== -1) {
                    this.excluded.splice(nameIndex, 1);
                    event.target.remove();
                    this.deleteNameInput(nameId, false);
                }
            }
        }
    }

    deleteNameWithIndex(nameId, included) {
        if (included) {
            const nameElement = document.querySelector(`.selected-name_included[data-name="${nameId}"]`);
            nameElement.remove();
        } else {
            const nameElement = document.querySelector(`.selected-name_excluded[data-name="${nameId}"]`);
            nameElement.remove();
        }
    }

    deleteNameInput(nameId, included) {
        if (included) {
            const nameElement = document.querySelector(`.hidden-input_included[data-name="${nameId}"]`);
            nameElement.remove();
        } else {
            const nameElement = document.querySelector(`.hidden-input_excluded[data-name="${nameId}"]`);
            nameElement.remove();
        }
    }

    async submitForm(event) {
        event.preventDefault();

        let nameOnData = [];
        let nameOffData = [];

        this.included.forEach((name) => {
            nameOnData.push(name.id);
        });

        this.excluded.forEach((name) => {
            nameOffData.push(name.id);
        });

        const formData = [];

        nameOnData.forEach((id) => {
            formData.push([this.includedFieldName, id]);
        })

        nameOffData.forEach((id) => {
            formData.push([this.excludedFieldName, id]);
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
        const selectedSkillElement = document.getElementById(`selectedNames${this.formName}`);
        const hiddenInputsElement = document.getElementById(`hiddenInputs${this.formName}`);
        selectedSkillElement.innerHTML = '';
        hiddenInputsElement.innerHTML = '';
        this.included = [];
        this.excluded = [];
    }

    createHTML() {
        const searchFieldset = document.getElementById(`searchForm${this.formName}`);

        searchFieldset.innerHTML = `
          <legend class="form-specs__legend">Search by ${this.formName}:</legend>
          <p class="form-specs__prompt">Click "+" to include the name to the search, click "-" to exclude the name
            from
            the search. Click on a name to remove it from the search.</p>
          <div class="form-specs__hidden-inputs" id="hiddenInputs${this.formName}"></div>
          <div class="form-specs__selected-names" id="selectedNames${this.formName}"></div>
          <div class="form-specs__search-wrapper">
            <label>
              <input class="form-specs__search" type="search" placeholder="Search" autocomplete="off" id="searchInput${this.formName}">
            </label>
            <ul class="form-specs__autocomplete-container autocomplete-list" id="autocompleteList${this.formName}">
            </ul>
            <div class="overlay" id="overlay${this.formName}"></div>
          </div>
        `;
    }

    startAutocomplete() {
        const searchInput = document.getElementById(`searchInput${this.formName}`);
        const overlay = document.getElementById(`overlay${this.formName}`);
        const selectedSkillElement = document.getElementById(`selectedNames${this.formName}`);
        const searchForm = document.querySelector('.form-specs');

        searchInput.addEventListener('input', this.filterForNames);
        searchInput.addEventListener('focus', this.filterForNames);
        overlay.addEventListener('click', this.closeContainer);
        selectedSkillElement.addEventListener('click', this.deleteNameWithEvent);
        searchForm.addEventListener('reset', this.clearAll);
    }
}
