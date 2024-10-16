import { Status } from './enum/status.enum';

export class ApiResponse<T> {
  result: T;
  status: Status;

  constructor(result: T, status: Status) {
    this.result = result;
    this.status = status;
  }
}
