import { createClient, print } from 'redis';
import { promisify } from 'util';

const client = createClient();

client.on('connect', () => {
  console.log('Redis client connected to the server');
});

client.on('error', (error) => {
  console.log('Redis client not connected to the server:', error);
});

const getAsync = promisify(client.get).bind(client);

function setNewSchool(schoolName, value) {
  client.set(schoolName, value, print);
}

async function displaySchoolValue(schoolName) {
  try {
    const value = await getAsync(schoolName);
    console.log(value);
  } catch (error) {
    console.error(error);
  }
}

displaySchoolValue('ALX');
setNewSchool('ALXSanFrancisco', '100');
displaySchoolValue('ALXSanFrancisco');
