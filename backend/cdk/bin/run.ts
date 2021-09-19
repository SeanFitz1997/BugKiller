#!/usr/bin/env node
import "source-map-support/register";
import * as cdk from "@aws-cdk/core";
import { BugKillerBackendApp } from "../lib/bugKillerBackendApp";

const app = new cdk.App();
new BugKillerBackendApp(app, "BugKillerBackend");
