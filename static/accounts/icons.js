export let expandSvg = `
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="2.5em" height="2.5em">
<style>
    path { fill: black; }

    @media (prefers-color-scheme: dark) {
        path { fill: white; }
    }
</style>
<path d="m12 5.83 2.46 2.46c.39.39 1.02.39 1.41 0 .39-.39.39-1.02 0-1.41L12.7 3.7a.9959.9959 0 0 0-1.41 0L8.12 6.88c-.39.39-.39 1.02 0 1.41.39.39 1.02.39 1.41 0L12 5.83zm0 12.34-2.46-2.46a.9959.9959 0 0 0-1.41 0c-.39.39-.39 1.02 0 1.41l3.17 3.18c.39.39 1.02.39 1.41 0l3.17-3.17c.39-.39.39-1.02 0-1.41a.9959.9959 0 0 0-1.41 0L12 18.17z"></path>
</svg>
`

export let collapseSvg = `
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="2.5em" height="2.5em">
<style>
    path { fill: black; }
    
    @media (prefers-color-scheme: dark) {
        path { fill: white; }
    }
</style>
<path d="M8.12 19.3c.39.39 1.02.39 1.41 0L12 16.83l2.47 2.47c.39.39 1.02.39 1.41 0 .39-.39.39-1.02 0-1.41l-3.17-3.17a.9959.9959 0 0 0-1.41 0l-3.17 3.17c-.4.38-.4 1.02-.01 1.41zm7.76-14.6a.9959.9959 0 0 0-1.41 0L12 7.17 9.53 4.7a.9959.9959 0 0 0-1.41 0c-.39.39-.39 1.03 0 1.42l3.17 3.17c.39.39 1.02.39 1.41 0l3.17-3.17c.4-.39.4-1.03.01-1.42z"></path>
</svg>
`
