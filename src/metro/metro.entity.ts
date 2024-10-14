export class Metro {
  id: number;
  lat: number;
  lon: number;
  name: string;
  station_code?: string;
  platform_type: string;
  line: string[];
  created_at: Date;
  updated_at: Date;
}
