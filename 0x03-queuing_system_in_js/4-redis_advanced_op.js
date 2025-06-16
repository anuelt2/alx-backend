import { createClient, print } from 'redis';

const client = createClient();

client.on('connect', () => {
  console.log('Redis client connected to the server');
});

client.on('error', (error) => {
  console.log('Redis client not connected to the server:', error);
});

client.del('ALX');

client.hset('ALX', 'Portland', 50, print);
client.hset('ALX', 'Seattle', 80, print);
client.hset('ALX', 'New York', 20, print);
client.hset('ALX', 'Bogota', 20, print);
client.hset('ALX', 'Cali', 40, print);
client.hset('ALX', 'Paris', 2, print);

client.hgetall('ALX', (error, obj) => {
  if (error) {
    console.error(error);
    return;
  }
  console.log(obj);
});
