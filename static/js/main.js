import {Autocomplete} from './Autocomplete.js';
import ServerApi from './ServerApi.js';

const autocomplete = new Autocomplete();
autocomplete.startAutocomplete();

const skills = await ServerApi.getSkills();

autocomplete.setSkills(skills);
