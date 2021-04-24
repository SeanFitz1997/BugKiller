#!/usr/bin/env node
import "source-map-support/register";
import * as cdk from "@aws-cdk/core";
import { FrontEndStack } from "../lib/frontend-stack";
import { APP_NAME } from "../lib/constants";

const app = new cdk.App();
new FrontEndStack(app, APP_NAME);
