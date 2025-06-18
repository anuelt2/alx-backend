import express from 'express';
import { createClient } from 'redis';
import kue from 'kue';
import { promisify } from 'util';

const app = express();
const port = 1245;
const queue = kue.createQueue();

// Redis
const client = createClient();
client.on('error', (error) => {
  console.error(error);
});

const getAsync = promisify(client.get).bind(client);
const setAsync = promisify(client.set).bind(client);

const RESERVATION_KEY = 'available_seats';
let reservationEnabled = true;

// Functions
async function reserveSeat(number) {
  await setAsync(RESERVATION_KEY, number);
}

async function getCurrentAvailableSeats() {
  const seats = await getAsync(RESERVATION_KEY);
  return parseInt(seats, 10);
}

reserveSeat(50);

// Routes
app.get('/available_seats', async (request, response) => {
  const seats = await getCurrentAvailableSeats();
  response.json({ numberOfAvailableSeats: seats.toString() });
});

app.get('/reserve_seat', (request, response) => {
  if (!reservationEnabled) {
    response.json({ status: "Reservation are blocked" });
  }

  const job = queue.create('reserve_seat');

  job.save((error) => {
    if (!error) {
      response.json({ status: 'Reservation in process' });
    } else {
      response.json({ status: 'Reservation failed' });
    }
  });

  job.on('complete', () => {
    console.log(`Seat reservation job ${job.id} completed`);
  });

  job.on('failed', (error) => {
    console.log(`Seat reservation job ${job.id} failed: ${error.message}`);
  });
});

app.get('/process', async (request, response) => {
  response.json({ status: 'Queue processing' });

  queue.process('reserve_seat', async (job, done) => {
    let seats = await getCurrentAvailableSeats();

    if (seats <= 0) {
      reservationEnabled = false;
      return done(new Error('Not enough seats available'));
    }

    seats -= 1;
    await reserveSeat(seats);

    if (seats === 0) {
      reservationEnabled = false;
    }

    done();
  });
});

app.listen(port);

export default app;
