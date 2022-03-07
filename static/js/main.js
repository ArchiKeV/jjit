import {Autocomplete} from './Autocomplete.js';
import ServerApi from './ServerApi.js';

const autocompleteSkills = new Autocomplete();
autocompleteSkills.setFormName('Skills');
autocompleteSkills.setExFieldName('skill_off_id');
autocompleteSkills.setInFieldName('skill_on_id');
autocompleteSkills.createHTML();

const autocompleteCompanies = new Autocomplete();
autocompleteCompanies.setFormName('Companies');
autocompleteCompanies.setExFieldName('company_off_id');
autocompleteCompanies.setInFieldName('company_on_id');
autocompleteCompanies.createHTML();

const companies = await ServerApi.getCompanies();
autocompleteCompanies.setNames(companies);
autocompleteCompanies.startAutocomplete();

const skills = await ServerApi.getSkills();
autocompleteSkills.setNames(skills);
autocompleteSkills.startAutocomplete();
