/**
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing,
 * software distributed under the License is distributed on an
 * "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
 * KIND, either express or implied.  See the License for the
 * specific language governing permissions and limitations
 * under the License.
 */

const TRUSTED_URLS_KEY = 'superset_trusted_urls';
const MAX_TRUSTED_URLS = 100;
const ALLOWED_SCHEMES = ['http:', 'https:'];

/**
 * Normalize a URL for comparison (origin + path without trailing slash + search).
 */
function normalizeUrl(url: string): string {
  try {
    const parsed = new URL(url);
    return parsed.origin + parsed.pathname.replace(/\/$/, '') + parsed.search;
  } catch {
    return url;
  }
}

/**
 * Produce a one-way numeric fingerprint of a string so that raw URLs
 * (which may carry tokens or session ids in query parameters) are
 * never persisted in clear text in localStorage.
 *
 * Uses the cyrb53 algorithm — a fast, well-distributed 53-bit hash.
 */
function fingerprintUrl(str: string): string {
  let h1 = 0xdeadbeef;
  let h2 = 0x41c6ce57;
  for (let i = 0; i < str.length; i += 1) {
    const ch = str.charCodeAt(i);
    h1 = Math.imul(h1 ^ ch, 2654435761);
    h2 = Math.imul(h2 ^ ch, 1597334677);
  }
  h1 = Math.imul(h1 ^ (h1 >>> 16), 2246822507);
  h1 ^= Math.imul(h2 ^ (h2 >>> 13), 3266489909);
  h2 = Math.imul(h2 ^ (h2 >>> 16), 2246822507);
  h2 ^= Math.imul(h1 ^ (h1 >>> 13), 3266489909);
  return (4294967296 * (2097151 & h2) + Math.trunc(h1)).toString(36);
}

/**
 * Return true if the URL scheme is safe for navigation.
 * Blocks javascript:, data:, vbscript:, file:, etc.
 */
export function isAllowedScheme(url: string): boolean {
  try {
    const parsed = new URL(url);
    return ALLOWED_SCHEMES.includes(parsed.protocol);
  } catch {
    // relative URLs or unparseable — allow (they'll resolve against current origin)
    return true;
  }
}

/**
 * Read the target URL from the current page's query string.
 *
 * URLSearchParams.get() already percent-decodes the value, so we must NOT
 * call decodeURIComponent again (doing so would allow double-encoded
 * payloads like `javascript%253Aalert(1)` to bypass scheme checks).
 */
export function getTargetUrl(): string {
  const params = new URLSearchParams(window.location.search);
  const url = params.get('url') ?? '';
  return url.trim();
}

function getTrustedFingerprints(): string[] {
  try {
    const stored = localStorage.getItem(TRUSTED_URLS_KEY);
    if (!stored) return [];
    const parsed: unknown = JSON.parse(stored);
    return Array.isArray(parsed) ? (parsed as string[]) : [];
  } catch {
    return [];
  }
}

function saveTrustedFingerprints(fingerprints: string[]): void {
  const limited =
    fingerprints.length > MAX_TRUSTED_URLS
      ? fingerprints.slice(-MAX_TRUSTED_URLS)
      : fingerprints;
  try {
    localStorage.setItem(TRUSTED_URLS_KEY, JSON.stringify(limited));
  } catch {
    // Ignore storage errors (private browsing, quota exceeded, etc.)
  }
}

export function isUrlTrusted(url: string): boolean {
  const fp = fingerprintUrl(normalizeUrl(url));
  return getTrustedFingerprints().includes(fp);
}

export function trustUrl(url: string): void {
  const fp = fingerprintUrl(normalizeUrl(url));
  const trusted = getTrustedFingerprints();
  if (!trusted.includes(fp)) {
    trusted.push(fp);
    saveTrustedFingerprints(trusted);
  }
}
