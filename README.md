# Experimental Feature

This fork introduces BatchSession, an extension of Requests that enables batching HTTP requests before execution.

Motivation:
Web scrapers often need to perform thousands of independent HTTP requests. BatchSession provides a familiar Requests API while allowing queued execution and future parallelization.gi