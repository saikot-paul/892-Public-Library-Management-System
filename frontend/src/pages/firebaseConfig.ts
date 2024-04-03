import {initializeApp} from 'firebase/app'
import config from './config'
import { getFirestore } from 'firebase/firestore'; // Import getFirestore

const app = initializeApp(config)
const firestore = getFirestore(app);

export { app, firestore };

//export {app}