import { DataSource } from 'typeorm';
import * as dotenv from 'dotenv';

dotenv.config();

export const databaseProviders = [
  {
    provide: 'DATA_SOURCE',
    useFactory: async () => {
      const dataSource = new DataSource({
        type: 'postgres',
        host: process.env.DJANGO_DB_HOST,
        port: parseInt(process.env.DJANGO_DB_PORT, 10),
        username: process.env.DJANGO_DB_USER,
        password: process.env.DJANGO_DB_PASSWORD,
        database: process.env.DJANGO_DB_NAME,
        entities: [__dirname + '/../**/*.entity{.ts,.js}'],
        // TODO fix: Setting synchronize: true shouldn't be used in production - otherwise you can lose production data.
        synchronize: true,
      });

      return dataSource.initialize();
    },
  },
];
