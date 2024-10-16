import { DataSource } from 'typeorm';
import { Metro } from './metro.entity';

export const metroProviders = [
  {
    provide: 'METRO_REPOSITORY',
    useFactory: (dataSource: DataSource) => dataSource.getRepository(Metro),
    inject: ['DATA_SOURCE'],
  },
];
