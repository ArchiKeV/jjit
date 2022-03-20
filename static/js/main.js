import {Autocomplete} from './Autocomplete.js';
import ServerApi from './ServerApi.js';
import {companiesVisa} from './companiesVisa.js';

const autocompleteSkills = new Autocomplete();
autocompleteSkills.setFormName('Skills');
autocompleteSkills.setExFieldName('skill_off');
autocompleteSkills.setInFieldName('skill_on');
autocompleteSkills.createHTML();

const autocompleteCompanies = new Autocomplete();
autocompleteCompanies.setFormName('Companies');
autocompleteCompanies.setExFieldName('company_off');
autocompleteCompanies.setInFieldName('company_on');
autocompleteCompanies.createHTML();

const companies = await ServerApi.getCompanies();
autocompleteCompanies.setNames(companies);
autocompleteCompanies.startAutocomplete();

const skills = await ServerApi.getSkills();
autocompleteSkills.setNames(skills);
autocompleteSkills.startAutocomplete();

autocompleteCompanies.setVisaNames(companiesVisa);
autocompleteCompanies.createVisaCompaniesButton();
