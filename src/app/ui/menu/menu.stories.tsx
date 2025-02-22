import type { Meta, StoryObj } from '@storybook/react';
import { fn } from '@storybook/test';

import Menu from './menu';


const meta = {
    title: 'Menu/Menu',
    component: Menu,
    tags: ['autodocs'],
} satisfies Meta<typeof Menu>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Primary: Story = {};
