import { Module } from '@nestjs/common';
import { AppController } from './app.controller';
import { AppService } from './app.service';
import { MetroModule } from './metro/metro.module';

@Module({
  imports: [MetroModule],
  controllers: [AppController],
  providers: [AppService],
})
export class AppModule {}
