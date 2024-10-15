export class Metro {
  id: number;
  lat: number;
  lon: number;
  name: string;
  station_code?: string;
  line: string[];
  created_at: number;
  updated_at: number;
}

export class MetroDto {
  id: number;
  lat: number;
  lon: number;
  name: string;
  station_code?: string;
  line: string[];
  created_at: number;
  updated_at: number;
}
