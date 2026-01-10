```php
$saga = new Workflow\Saga();

$carReservationID = yield $this->activities->reserveCar($name);
$saga->addCompensation(fn() => yield $this->activities->cancelCar($carReservationID, $name));

$hotelReservationID = yield $this->activities->bookHotel($name);
$saga->addCompensation(fn() => yield $this->activities->cancelHotel($hotelReservationID, $name));

$flightReservationID = yield $this->activities->bookFlight($name);
$saga->addCompensation(fn() => yield $this->activities->cancelFlight($flightReservationID, $name));
```