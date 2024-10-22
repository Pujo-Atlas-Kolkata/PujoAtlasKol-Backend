import { NestFactory } from '@nestjs/core';
import { AppModule } from './app.module';
import * as dotenv from 'dotenv';
import { join } from 'path';
dotenv.config({ path: process.cwd() + '/.env.development' }); 

async function bootstrap() {
  
  const app = await NestFactory.create(AppModule);
  await app.listen(3000);
}
bootstrap();