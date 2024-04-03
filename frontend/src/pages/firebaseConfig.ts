import {initializeApp} from 'firebase/app'
import config from './config'

const app = initializeApp(config)

export {app}